/**
 * 统一社会信用代码 (USCC, GB 32100-2015) 前端校验。
 *
 * 算法必须与后端 `backend/app/core/uscc.py` 完全一致 —— 标准即契约。
 * 18 位结构：登记管理部门码(1) + 机构类别码(1) + 行政区划码(6) + 主体标识码(9) + 校验码(1)。
 * 字符集剔除易混淆的 I / O / S / V / Z，共 31 个字符。
 */

/** 官方字符集（31 个） */
export const USCC_CHARSET = '0123456789ABCDEFGHJKLMNPQRTUWXY';

/** 校验位权重（17 位，对应前 17 位主体码） */
export const USCC_WEIGHTS = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28];

const USCC_PATTERN = /^[0-9A-HJ-NPQRTUWXY]{18}$/;

/**
 * 录入归一化：去空白（含全角空格）与连字符、转大写。
 * 空值一律返回 ''，便于调用方用「是否为空」判断是否填写。
 *
 * 注意：这里**不做** I/O/S/V/Z 的自动替换 —— 它们在 USCC 里只可能是录入错误，
 * 静默改写会把错误藏起来，应由校验层显式提示用户核对。
 */
export function normalizeUscc(value) {
  if (value === null || value === undefined) return '';
  return String(value)
    .replace(/\s/g, '')
    .replace(/　/g, '')
    .replace(/-/g, '')
    .trim()
    .toUpperCase();
}

/** 仅形态校验：18 位、合法字符集 */
export function isUsccFormat(uscc) {
  return !!uscc && USCC_PATTERN.test(uscc);
}

/** 由前 17 位推导校验字符 */
function checksumChar(body17) {
  let total = 0;
  for (let i = 0; i < 17; i += 1) {
    total += USCC_CHARSET.indexOf(body17[i]) * USCC_WEIGHTS[i];
  }
  return USCC_CHARSET[(31 - (total % 31)) % 31];
}

/** 校验位是否正确（含形态校验） */
export function usccChecksumOk(uscc) {
  if (!isUsccFormat(uscc)) return false;
  return checksumChar(uscc.slice(0, 17)) === uscc[17];
}

/** 完整合法性：形态 + 校验位 */
export function isValidUscc(value) {
  const normalized = normalizeUscc(value);
  if (!normalized) return false;
  return usccChecksumOk(normalized);
}

/**
 * 校验并给出中文原因。通过时返回 null。
 * 未填写（空串）视为"未使用 USCC"，返回 null 而非错误 —— 这是可选字段。
 */
export function usccErrorMessage(value) {
  const normalized = normalizeUscc(value);
  if (!normalized) return null;
  if (!isUsccFormat(normalized)) {
    return '应为 18 位大写字母与数字，且不含易混淆字符 I / O / S / V / Z';
  }
  if (!usccChecksumOk(normalized)) {
    return '校验位不正确，请核对后重新录入';
  }
  return null;
}

/** 已填写但不合法 —— 用于提交前拦截（未填写返回 false） */
export function isUsccFilledButInvalid(value) {
  const normalized = normalizeUscc(value);
  return !!normalized && usccErrorMessage(normalized) !== null;
}

/**
 * 由前 17 位补全校验位（仅用于测试样本构造与录入辅助，勿用于生产数据改写）。
 */
export function completeUscc(body17) {
  if (!/^[0-9A-HJ-NPQRTUWXY]{17}$/.test(body17 || '')) {
    throw new Error('前 17 位必须为大写字母与数字，且不含 I/O/S/V/Z');
  }
  return body17 + checksumChar(body17);
}
