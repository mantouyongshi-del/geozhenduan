# -*- coding: utf-8 -*-
import time
import httpx
import logging
from app.adapters.base import BaseModelAdapter, AdapterResponse
from app.core.config import settings

logger = logging.getLogger("HunyuanAdapter")

class HunyuanAdapter(BaseModelAdapter):
    def __init__(self):
        super().__init__(
            provider="hunyuan",
            provider_name="腾讯科技 · 腾讯元宝/混元",
            model_name="hy3"
        )
        self.api_url = "https://tokenhub.tencentmaas.com/v1/chat/completions"

    async def query(self, query_text: str, search_enabled: bool = True) -> AdapterResponse:
        start_t = time.time()
        api_key = settings.HUNYUAN_API_KEY
        if not api_key:
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message="未配置 HUNYUAN_API_KEY"
            )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        system_msg = "你是腾讯元宝人工智能助手，依托腾讯混元内核与微信社交公域生态，为用户提供客观严谨的决策参考。"
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": query_text}
            ],
            "temperature": 0.5,
            "max_tokens": 1500
        }

        try:
            async with httpx.AsyncClient(trust_env=False, timeout=35.0) as client:
                resp = await client.post(self.api_url, headers=headers, json=payload)
                latency = int((time.time() - start_t) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    content = choices[0]["message"]["content"] if choices else ""
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
            logger.error(f"混元调用失败: {e}")
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message=str(e)
            )
