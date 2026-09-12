"""补列迁移离线测试套件（最容易被写假的环节，全部真实断言）。

策略：用裸 sqlite3 造一个「历史旧版库」（companies 表无 uscc），
再用独立 engine 跑 ensure_schema，断言补列、幂等、空库安全、索引、数据无损、ORM 可用。

严格禁止使用 pytest 的 tmp_path fixture（受限文件系统下基目录复用会误抛 PermissionError），
一律用 tempfile.mkdtemp() 自建临时目录。
"""
from __future__ import annotations

import os
import sqlite3
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as DBSession
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.migrations import describe_pending_columns, ensure_schema
from app.models.company import Company


OLD_COMPANY_NAME = "长沙岳麓万豪酒店管理有限公司"


def _make_legacy_db(path: str) -> None:
    """用裸 sqlite3 造一个不带 uscc 的旧版 companies 表，并插入一行真实数据。"""
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            """
            CREATE TABLE companies (
                id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                short_name VARCHAR(100),
                logo_url VARCHAR(500),
                industry VARCHAR(100),
                brand_aliases TEXT NOT NULL,
                is_active BOOLEAN,
                created_at INTEGER,
                updated_at INTEGER
            )
            """
        )
        conn.execute(
            """
            INSERT INTO companies
                (id, name, short_name, logo_url, industry, brand_aliases, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (1, OLD_COMPANY_NAME, "万豪", None, "酒店",
             "万豪酒店, 万豪", 1, 1700000000, 1700000000),
        )
        conn.commit()
    finally:
        conn.close()


@pytest.fixture
def legacy_engine():
    d = tempfile.mkdtemp(prefix="uscc_mig_")
    path = os.path.join(d, "legacy_geo_system.db")
    _make_legacy_db(path)
    eng = create_engine(f"sqlite:///{path}")
    yield eng
    eng.dispose()


def _table_columns(path: str, table: str):
    conn = sqlite3.connect(path)
    try:
        return [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]
    finally:
        conn.close()


def test_pending_before_migration(legacy_engine):
    """迁移前：describe_pending_columns 应探测到 ('companies', 'uscc')。"""
    pending = describe_pending_columns(legacy_engine)
    assert ("companies", "uscc") in pending


def test_ensure_schema_adds_uscc(legacy_engine):
    """ensure_schema 返回列表含 ('companies','uscc')。"""
    actions = ensure_schema(legacy_engine)
    assert ("companies", "uscc") in actions


def test_uscc_column_exists_after_migration(legacy_engine):
    """迁移后：PRAGMA table_info 确认 uscc 列已存在。"""
    ensure_schema(legacy_engine)
    path = legacy_engine.url.database
    cols = _table_columns(path, "companies")
    assert "uscc" in cols


def test_historical_data_preserved(legacy_engine):
    """迁移不能毁数据：插入的那一行仍然可查，且 name 一致。"""
    ensure_schema(legacy_engine)
    path = legacy_engine.url.database
    conn = sqlite3.connect(path)
    try:
        rows = conn.execute("SELECT id, name FROM companies").fetchall()
        assert len(rows) == 1
        assert rows[0][1] == OLD_COMPANY_NAME
    finally:
        conn.close()


def test_idempotent_rerun(legacy_engine):
    """幂等：再次 ensure_schema 返回空（或不含 uscc），describe_pending_columns 为 []。"""
    ensure_schema(legacy_engine)
    second = ensure_schema(legacy_engine)
    assert ("companies", "uscc") not in second
    assert describe_pending_columns(legacy_engine) == []


def test_empty_db_safe(legacy_engine):
    """空库安全：全新空 SQLite（无任何表），ensure_schema 返回 [] 且不抛异常。"""
    d = tempfile.mkdtemp(prefix="uscc_empty_")
    path = os.path.join(d, "empty.db")
    sqlite3.connect(path).close()  # 仅建空文件，无任何表
    eng = create_engine(f"sqlite:///{path}")
    try:
        result = ensure_schema(eng)
        assert result == []
    finally:
        eng.dispose()


def test_index_created_after_migration(legacy_engine):
    """迁移后索引已建：sqlite_master 能查到 ix_companies_uscc。"""
    ensure_schema(legacy_engine)
    path = legacy_engine.url.database
    conn = sqlite3.connect(path)
    try:
        idx = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='companies'"
        )]
        assert "ix_companies_uscc" in idx
    finally:
        conn.close()


def test_orm_readable_after_migration(legacy_engine):
    """ORM 可用：迁移后绑定该 engine 查询 Company，正常读出且 uscc is None。"""
    ensure_schema(legacy_engine)
    Session = sessionmaker(bind=legacy_engine)
    with DBSession(legacy_engine) as s:
        rows = s.query(Company).all()
        assert len(rows) == 1
        company = rows[0]
        assert company.name == OLD_COMPANY_NAME
        assert company.uscc is None  # 旧数据补列后应为 NULL，不再 no such column
