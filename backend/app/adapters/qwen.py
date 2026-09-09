# -*- coding: utf-8 -*-
import time
import httpx
import logging
from app.adapters.base import BaseModelAdapter, AdapterResponse
from app.core.config import settings

logger = logging.getLogger("QwenAdapter")

class QwenAdapter(BaseModelAdapter):
    def __init__(self):
        super().__init__(
            provider="qwen",
            provider_name="阿里巴巴 · 通义千问",
            model_name="qwen-turbo"
        )
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    async def query(self, query_text: str, search_enabled: bool = True) -> AdapterResponse:
        start_t = time.time()
        api_key = settings.DASHSCOPE_API_KEY or settings.QWEN_API_KEY
        if not api_key:
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message="未配置 DASHSCOPE_API_KEY"
            )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        system_msg = "你是通义千问，依托阿里云百炼全网原生联网检索生态，为用户提供客观严谨的行业决策与真实信源解答。"
        payload = {
            "model": self.model_name,
            "input": {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": query_text}
                ]
            },
            "parameters": {
                "enable_search": search_enabled,
                "search_options": {"enable_source": True},
                "result_format": "message"
            }
        }

        try:
            async with httpx.AsyncClient(trust_env=False, timeout=30.0) as client:
                resp = await client.post(self.api_url, headers=headers, json=payload)
                latency = int((time.time() - start_t) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    output = data.get("output", {})
                    choices = output.get("choices", [])
                    content = choices[0]["message"]["content"] if choices else ""

                    # 解析原生联网检索信源 (手机端同款信源)
                    raw_cites = output.get("search_info", {}).get("search_results", [])
                    citations = []
                    for c in raw_cites:
                        citations.append({
                            "title": c.get("title", ""),
                            "url": c.get("url", ""),
                            "site_name": c.get("site_name") or "权威资讯",
                            "summary": c.get("title", "")
                        })

                    return AdapterResponse(
                        provider=self.provider,
                        provider_name=self.provider_name,
                        model_name=self.model_name,
                        query=query_text,
                        raw_text=content,
                        citations=citations,
                        search_enabled=search_enabled,
                        observability_level="high",  # 原生支持完整搜索溯源
                        latency_ms=latency,
                        status="success"
                    )
                else:
                    return AdapterResponse(
                        provider=self.provider,
                        provider_name=self.provider_name,
                        model_name=self.model_name,
                        query=query_text,
                        raw_text="",
                        latency_ms=latency,
                        status="error",
                        error_message=f"HTTP {resp.status_code}: {resp.text[:100]}"
                    )
        except Exception as e:
            logger.error(f"千问调用失败: {e}")
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message=str(e)
            )
