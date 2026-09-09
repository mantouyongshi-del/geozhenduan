# -*- coding: utf-8 -*-
"""
统一模型适配器抽象基类与响应规范 (Base Model Adapter)
遵循《AI 品牌可见性与推荐检测系统方案》第 609-686 行技术规范
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


@dataclass
class AdapterResponse:
    provider: str                           # 平台标识: doubao, qwen, deepseek, kimi, hunyuan, baidu
    provider_name: str                      # 平台展示名
    model_name: str                         # 底层模型型号
    query: str                              # 实际提问
    raw_text: str                           # 原始返回文本
    citations: List[Dict[str, str]] = field(default_factory=list)  # 引用的客观权威信源
    search_enabled: bool = True             # 是否开启联网检索
    observability_level: str = "medium"     # 可观测性等级: high(支持全信源溯源), medium(部分元数据), low(黑盒回答)
    latency_ms: int = 0                     # 请求耗时 (毫秒)
    status: str = "success"                 # 状态: success / error
    error_message: Optional[str] = None     # 错误信息


class BaseModelAdapter(ABC):
    """大模型标准化适配器抽象基类"""

    def __init__(self, provider: str, provider_name: str, model_name: str):
        self.provider = provider
        self.provider_name = provider_name
        self.model_name = model_name

    @abstractmethod
    async def query(self, query_text: str, search_enabled: bool = True) -> AdapterResponse:
        """
        向被测大模型发起纯净的自然消费者提问。
        【铁律】：仅传入自然提问，绝对禁止在 Prompt 中私自夹带、预设竞品或做假兜底！
        """
        pass
