# -*- coding: utf-8 -*-
import time
import asyncio
import httpx
import logging
from app.adapters.base import BaseModelAdapter, AdapterResponse
from app.core.config import settings

logger = logging.getLogger("KimiAdapter")

class KimiAdapter(BaseModelAdapter):
    _semaphore = None

    @classmethod
    def _get_semaphore(cls):
        if cls._semaphore is None:
            cls._semaphore = asyncio.Semaphore(1)
        return cls._semaphore

    def __init__(self):
        super().__init__(
            provider="kimi",
            provider_name="月之暗面 · Moonshot Kimi",
            model_name="kimi-k2.6"
        )
        self.api_url = "https://api.moonshot.cn/v1/chat/completions"

    async def query(self, query_text: str, search_enabled: bool = True) -> AdapterResponse:
        start_t = time.time()
        api_key = settings.MOONSHOT_API_KEY
        if not api_key:
            return AdapterResponse(
                provider=self.provider,
                provider_name=self.provider_name,
                model_name=self.model_name,
                query=query_text,
                raw_text="",
                status="error",
                error_message="未配置 MOONSHOT_API_KEY"
            )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        system_msg = "你是一个严谨客观、注重事实查证与长文本研判的第三方智能搜索专家。请客观如实回答用户提问。"
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": query_text}
            ],
            "max_tokens": 2000,
            "thinking": {"type": "disabled"}
        }

        max_retries = 2
        sem = self._get_semaphore()
        async with sem:
            for attempt in range(max_retries + 1):
                try:
                    async with httpx.AsyncClient(trust_env=False, timeout=60.0) as client:
                        resp = await client.post(self.api_url, headers=headers, json=payload)
                        latency = int((time.time() - start_t) * 1000)
                        if resp.status_code == 200:
                            data = resp.json()
                            msg = data["choices"][0]["message"]
                            content = msg.get("content", "")
                            reasoning = msg.get("reasoning_content", "")
                            if reasoning:
                                content = f"> **Kimi 长文本考证推理过程:**\n> {reasoning}\n\n{content}"

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
                        elif resp.status_code == 429 and attempt < max_retries:
                            # 触发组织并发限流，等待 2 秒后自动重试
                            logger.warning(f"Kimi 触发并发限频 (429)，将在 2 秒后进行第 {attempt + 1} 次重试...")
                            await asyncio.sleep(2.0)
                            continue
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
                    if attempt < max_retries:
                        await asyncio.sleep(1.5)
                        continue
                    logger.error(f"Kimi 调用失败: {e}")
                    return AdapterResponse(
                        provider=self.provider,
                        provider_name=self.provider_name,
                        model_name=self.model_name,
                        query=query_text,
                        raw_text="",
                        status="error",
                        error_message=str(e)
                    )

        return AdapterResponse(
            provider=self.provider,
            provider_name=self.provider_name,
            model_name=self.model_name,
            query=query_text,
            raw_text="",
            status="error",
            error_message="重试后依然超时或受限"
        )
