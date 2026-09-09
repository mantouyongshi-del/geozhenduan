# -*- coding: utf-8 -*-
import time
import httpx
import logging
from app.adapters.base import BaseModelAdapter, AdapterResponse
from app.core.config import settings

logger = logging.getLogger("DoubaoAdapter")

class DoubaoAdapter(BaseModelAdapter):
    def __init__(self):
        super().__init__(
            provider="doubao",
            provider_name="字节跳动 · 豆包",
            model_name=settings.DOUBAO_MODEL_NAME or "doubao-seed-2-0-mini-260215"
        )
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    async def query(self, query_text: str, search_enabled: bool = True) -> AdapterResponse:
        start_t = time.time()
        api_key = settings.DOUBAO_API_KEY
        if not api_key:
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message="未配置 DOUBAO_API_KEY"
            )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        system_msg = "你是字节跳动官方人工智能大模型豆包，深度融合抖音内容生态与全网事实，为用户提供客观严谨的选型推荐。"
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": query_text}
            ],
            "max_tokens": 2500
        }

        try:
            async with httpx.AsyncClient(trust_env=False, timeout=40.0) as client:
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
            logger.error(f"豆包调用失败: {e}")
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message=str(e)
            )
