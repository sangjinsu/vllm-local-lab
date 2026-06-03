from __future__ import annotations

from openai import OpenAI

from vllm_lab.config import Settings, settings


def create_client(config: Settings = settings) -> OpenAI:
    return OpenAI(
        base_url=config.vllm_base_url,
        api_key=config.vllm_api_key,
    )
