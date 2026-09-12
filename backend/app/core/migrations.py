"""SQLite 轻量幂等补列迁移。

## 为什么需要它

`Base.metadata.create_all()` 只创建**缺失的表**，对已存在的表**完全不做任何变更**
（SQLAlchemy 的既定语义，不是 bug）。而本仓库有历史库在跑（`backend/geo_system.db`
已有的 `companies` 表就没有 `uscc` 列），一旦给模型加字段而不补列，所有相关查询
都会抛 `sqlite3.OperationalError: no such column`，接口直接 500。

本项目刻意不引入 Alembic：三仓均为单体轻量服务，单文件 SQLite，
"启动时对比 ORM 元数据与实际表结构、按需补列" 已足够，且零额外依赖、零运维步骤。

## 行为边界

- **只补列**，不删列、不改类型、不重命名 —— 破坏性变更必须人工处理。
- **只补可空列**。SQLite 无法给已有数据行补一个「非空且无默认值」的列，
  遇到这种列会告警跳过（而不是让整个启动崩掉）。
- 幂等：列已存在则跳过，重复启动无副作用。
- 非 SQLite 后端（如 PostgreSQL）同样可用，`inspect()` 是方言无关的。
"""
from __future__ import annotations

import logging
from typing import List, Tuple

from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.schema import CreateColumn

from app.core.database import Base

logger = logging.getLogger(__name__)

__all__ = ["ensure_schema", "describe_pending_columns"]


def _safe_inspect(engine: Engine):
    return inspect(engine)


def describe_pending_columns(engine: Engine) -> List[Tuple[str, str]]:
    """只读探测：返回「ORM 有、但实际库缺失」的 (表名, 列名) 列表，不做任何写入。

    供测试与运维自检使用（可在不连写权限的情况下判断是否需要迁移）。
    """
    inspector = _safe_inspect(engine)
    existing_tables = set(inspector.get_table_names())
    missing: List[Tuple[str, str]] = []
    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue
        existing_cols = {c["name"] for c in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name not in existing_cols:
                missing.append((table.name, column.name))
    return missing


def ensure_schema(engine: Engine) -> List[Tuple[str, str]]:
    """对比 ORM 元数据与真实表结构，为已存在的表补齐缺失列与索引。

    返回实际执行的补列动作列表 `[(表名, 列名), ...]`，便于日志与测试断言。
    """
    inspector = _safe_inspect(engine)
    existing_tables = set(inspector.get_table_names())
    if not existing_tables:
        # 崭新的库：create_all 会按最新模型建全，无需补列
        return []

    added: List[Tuple[str, str]] = []

    # 第一步：收集全部待补列（先探测后写入，避免边遍历边改结构）
    pending: List[Tuple[str, object]] = []
    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue
        existing_cols = {c["name"] for c in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing_cols:
                continue
            if (
                not column.nullable
                and column.default is None
                and column.server_default is None
            ):
                logger.warning(
                    "[migration] 跳过 %s.%s：非空且无默认值，SQLite 无法为已有数据行补列；"
                    "请人工迁移或先赋予默认值",
                    table.name,
                    column.name,
                )
                continue
            pending.append((table.name, column))

    if not pending:
        return []

    # 第二步：逐条 ALTER TABLE（每条独立事务，单条失败不影响其余列）
    for table_name, column in pending:
        try:
            ddl = str(CreateColumn(column).compile(dialect=engine.dialect))
        except Exception as exc:  # noqa: BLE001
            logger.warning("[migration] 无法编译 %s.%s 的 DDL：%s", table_name, column.name, exc)
            continue
        try:
            with engine.begin() as conn:
                conn.exec_driver_sql(f'ALTER TABLE "{table_name}" ADD COLUMN {ddl}')
            added.append((table_name, column.name))
            logger.info("[migration] 已补列 %s.%s (%s)", table_name, column.name, ddl)
        except Exception as exc:  # noqa: BLE001 — 迁移失败绝不能让服务起不来
            message = str(exc).lower()
            if "duplicate column" in message or "already exists" in message:
                # 多进程并发启动时的良性竞争：另一进程已抢先补上，视为成功
                added.append((table_name, column.name))
                continue
            logger.error("[migration] 补列 %s.%s 失败：%s", table_name, column.name, exc)

    # 第三步：补索引（ALTER TABLE ADD COLUMN 不会带出索引，需单独建；checkfirst 保证幂等）
    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue
        for index in table.indexes:
            try:
                with engine.begin() as conn:
                    index.create(bind=conn, checkfirst=True)
            except Exception:  # noqa: BLE001 — 索引已存在等情况静默跳过
                pass

    return added
