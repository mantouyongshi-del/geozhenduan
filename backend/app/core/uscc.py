"""统一社会信用代码 (USCC, GB 32100-2015) 校验内核。

18 位结构：登记管理部门码(1) + 机构类别码(1) + 登记管理机关行政区划码(6) + 主体标识码(9) + 校验码(1)。
字符集剔除易混淆的 I / O / S / V / Z，共 31 个字符。

与 02-brand-knowledge 的 `app/schemas/uscc.py` 保持同一算法（标准即契约）。
本仓库独立实现以避免跨仓 import：三仓是独立部署单元，不允许代码级互相依赖。
"""
from __future__ import annotations

import re
from typing import Optional

USCC_CHARSET = "0123456789ABCDEFGHJKLMNPQRTUWXY"
USCC_WEIGHTS = (1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28)
USCC_PATTERN = re.compile(r"^[0-9A-HJ-NPQRTUWXY]{18}$")

def normalize_uscc(value: Optional[str]) -> Optional[str]:
    """录入归一化：去空白（含全角空格）、转大写；空串一律归为 None。

    注意：这里**不做**易混淆字符的自动替换 —— `I/O/S/Z` 出现在 USCC 里
    只可能是录入错误，静默改写会把错误藏起来，应由校验层显式拒绝。
    """
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    cleaned = value.replace(" ", "").replace("\u3000", "").replace("-", "").strip().upper()
    return cleaned or None


def is_uscc_format(uscc: str) -> bool:
    """仅做形态校验：长度 18、全大写字母与数字、不含 I/O/S/V/Z。"""
    return bool(uscc) and bool(USCC_PATTERN.match(uscc))


def _checksum_char(body17: str) -> str:
    total = sum(USCC_CHARSET.index(c) * w for c, w in zip(body17, USCC_WEIGHTS))
    return USCC_CHARSET[(31 - total % 31) % 31]


def uscc_checksum_ok(uscc: str) -> bool:
    """校验位 (第 18 位) 是否与 GB 32100 算法一致。"""
    if not is_uscc_format(uscc):
        return False
    return _checksum_char(uscc[:17]) == uscc[17]


def is_valid_uscc(uscc: Optional[str]) -> bool:
    """完整合法性校验（形态 + 校验位）。None / 空串一律为不合法。"""
    if not uscc:
        return False
    return uscc_checksum_ok(uscc)


def complete_uscc(body17: str) -> str:
    """由前 17 位推导校验位，用于数据录入补全与测试样本构造。"""
    if not re.fullmatch(r"[0-9A-HJ-NPQRTUWXY]{17}", body17 or ""):
        raise ValueError("前 17 位必须为大写字母与数字，且不含 I/O/S/V/Z")
    return body17 + _checksum_char(body17)


def validate_or_none(value: Optional[str]) -> Optional[str]:
    """写入路径的统一入口：合法则返回归一化后的 USCC，未填写返回 None。

    不合法时抛 `ValueError`（由 API 层转成 422 并给出可读原因）。
    设计取舍：**宁可显式报错，也不落脏数据**。一个校验位错误的 USCC 进了库，
    下游 03 会拿它去查 02 知识库而查不到，静默退化为兜底语料 —— 比降级主键更隐蔽。
    """
    normalized = normalize_uscc(value)
    if normalized is None:
        return None
    if not is_uscc_format(normalized):
        raise ValueError(
            "统一社会信用代码格式不正确：应为 18 位大写字母与数字，"
            "且不含易混淆字符 I / O / S / V / Z"
        )
    if not uscc_checksum_ok(normalized):
        raise ValueError("统一社会信用代码校验位不正确，请核对后重新录入")
    return normalized
