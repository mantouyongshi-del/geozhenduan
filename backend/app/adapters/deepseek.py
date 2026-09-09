# -*- coding: utf-8 -*-
import time
import httpx
import logging
from app.adapters.base import BaseModelAdapter, AdapterResponse
from app.core.config import settings

logger = logging.getLogger("DeepSeekAdapter")

class DeepSeekAdapter(BaseModelAdapter):
    def __init__(self):
        super().__init__(
            provider="deepseek",
            provider_name="深度求索 · DeepSeek",
            model_name="deepseek-chat"
        )
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    async def query(self, query_text: str, search_enabled: bool = True) -> AdapterResponse:
        start_t = time.time()
        api_key = settings.DEEPSEEK_API_KEY
        if not api_key:
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message="未配置 DEEPSEEK_API_KEY"
            )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        system_msg = "你是一个严谨客观的智能搜索助手与行业咨询顾问。请结合客观事实如实回答用户的问题。"
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": query_text}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }

        try:
            async with httpx.AsyncClient(trust_env=False, timeout=30.0) as client:
                resp = await client.post(self.api_url, headers=headers, json=payload)
                latency = int((time.time() - start_t) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    return AdapterResponse(
                        provider=self.provider,
                        provider_name=self.provider_name,
                        model_name=self.model_name,
                        query=query_text,
                        raw_text=content,
                        citations=[],
                        search_enabled=search_enabled,
                        observability_level="medium",
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
            logger.error(f"DeepSeek 被测调用失败: {e}")
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message=str(e)
            )
