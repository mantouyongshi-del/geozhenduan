# -*- coding: utf-8 -*-
from typing import Dict
from app.adapters.base import BaseModelAdapter, AdapterResponse
from app.adapters.doubao import DoubaoAdapter
from app.adapters.qwen import QwenAdapter
from app.adapters.deepseek import DeepSeekAdapter
from app.adapters.kimi import KimiAdapter
from app.adapters.hunyuan import HunyuanAdapter
from app.adapters.baidu import BaiduAdapter

def get_all_adapters() -> Dict[str, BaseModelAdapter]:
    """获取所有 6 大模型标准化适配器实例字典"""
    return {
        "doubao": DoubaoAdapter(),
        "qwen": QwenAdapter(),
        "deepseek": DeepSeekAdapter(),
        "kimi": KimiAdapter(),
        "hunyuan": HunyuanAdapter(),
        "baidu": BaiduAdapter()
    }
