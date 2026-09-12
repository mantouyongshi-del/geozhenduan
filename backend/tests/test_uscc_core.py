"""USCC 校验内核离线测试套件（GB 32100-2015）。

全部为纯函数级断言，不触网、不落库。
"""
from __future__ import annotations

import pytest

from app.core.uscc import (
    USCC_CHARSET,
    complete_uscc,
    is_uscc_format,
    is_valid_uscc,
    normalize_uscc,
    uscc_checksum_ok,
    validate_or_none,
)

# 任务给定的合法测试样本：由前 17 位推导出的完整 18 位 USCC
VALID_USCC = complete_uscc("91430100MA4L2X8K3")  # -> 91430100MA4L2X8K3T


def test_complete_uscc_sample_is_valid():
    """complete_uscc 构造的样本必须通过 形态+校验位 完整校验。"""
    assert len(VALID_USCC) == 18
    assert is_uscc_format(VALID_USCC) is True
    assert uscc_checksum_ok(VALID_USCC) is True
    assert is_valid_uscc(VALID_USCC) is True


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("91430100ma4l2x8k3t", VALID_USCC),   # 小写
        ("  91430100MA4L2X8K3T  ", VALID_USCC),  # 前后空格
        ("91430100 MA4L2X8K3 T", VALID_USCC),    # 中间空格
        ("\u300091430100MA4L2X8K3T", VALID_USCC),  # 前导全角空格
        ("91430100-MA4L2X8K3-T", VALID_USCC),     # 连字符
    ],
)
def test_normalize_uscc_variants(raw, expected):
    """录入归一化：小写/前后空格/中间空格/全角空格/连字符 → 同一大写值。"""
    assert normalize_uscc(raw) == expected


@pytest.mark.parametrize("empty", ["", None, "   ", "\u3000"])
def test_normalize_uscc_empty_returns_none(empty):
    """空串 / None / 纯空白 → None（USCC 是可选字段）。"""
    assert normalize_uscc(empty) is None


def test_validate_or_none_accepts_valid_without_rewrite():
    """零误杀负向：合法 USCC 必须被接受且值不被改写。"""
    out = validate_or_none(VALID_USCC)
    assert out == VALID_USCC
    # 小写形态传入也归一为同一大写值，且不被静默改写语义
    assert validate_or_none("91430100ma4l2x8k3t") == VALID_USCC


def test_validate_or_none_none_and_empty_return_none():
    """validate_or_none(None) 与 ('') 必须返回 None 而不抛异常（可选字段不填是合法路径）。"""
    assert validate_or_none(None) is None
    assert validate_or_none("") is None
    assert validate_or_none("   ") is None


def test_reject_wrong_length():
    """① 长度不对 → 拒绝，原因含「18 位」。"""
    with pytest.raises(ValueError) as exc:
        validate_or_none("123")
    assert "18 位" in str(exc.value)


def test_reject_confusing_chars():
    """② 含易混淆字符 I/O/S/V/Z → 拒绝，原因点名易混淆字符。"""
    # 18 位但末位为 I（字符集外的易混淆字符）
    bad = "12345678901234567I"
    assert is_uscc_format(bad) is False
    with pytest.raises(ValueError) as exc:
        validate_or_none(bad)
    assert "I / O / S / V / Z" in str(exc.value)


def test_reject_bad_checksum():
    """③ 长度对但校验位错（末位改成另一个合法字符）→ 拒绝，原因含「校验位」。"""
    # 把合法样本的末位 T 改成同样合法的 X，校验位即失效
    bad = VALID_USCC[:-1] + "X"
    assert is_uscc_format(bad) is True          # 形态仍过
    assert uscc_checksum_ok(bad) is False        # 校验位不过
    with pytest.raises(ValueError) as exc:
        validate_or_none(bad)
    assert "校验位" in str(exc.value)


def test_three_illegal_reasons_differ():
    """三类非法输入原因区分：格式错误（①②）与校验位错误（③）必须不同。"""
    with pytest.raises(ValueError) as e1:
        validate_or_none("123")                # ①
    with pytest.raises(ValueError) as e2:
        validate_or_none("12345678901234567I")  # ②
    with pytest.raises(ValueError) as e3:
        validate_or_none(VALID_USCC[:-1] + "X")  # ③
    r1, r2, r3 = str(e1.value), str(e2.value), str(e3.value)
    # ①② 同属「格式不正确」路径（实现契约），③ 走独立的校验位路径
    assert r1 == r2
    assert r3 != r1
    assert "校验位" in r3


def test_charset_excludes_confusing_chars():
    """防御性自检：字符集不得包含 I/O/S/V/Z。"""
    for ch in "IOSVZ":
        assert ch not in USCC_CHARSET
