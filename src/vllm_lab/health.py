from __future__ import annotations

from dataclasses import dataclass

import requests

from vllm_lab.config import Settings, settings


@dataclass(frozen=True)
class HealthResult:
    ok: bool
    endpoint: str
    status_code: int | None
    message: str


def server_root(base_url: str) -> str:
    return base_url.rstrip("/").removesuffix("/v1")


def check_health(config: Settings = settings, timeout_seconds: float = 5.0) -> HealthResult:
    endpoint = f"{server_root(config.vllm_base_url)}/health"
    try:
        response = requests.get(endpoint, timeout=timeout_seconds)
    except requests.RequestException as exc:
        return HealthResult(
            ok=False,
            endpoint=endpoint,
            status_code=None,
            message=f"vLLM server에 연결할 수 없습니다: {exc}",
        )

    if response.ok:
        return HealthResult(
            ok=True,
            endpoint=endpoint,
            status_code=response.status_code,
            message="vLLM server에 연결되었습니다.",
        )

    return HealthResult(
        ok=False,
        endpoint=endpoint,
        status_code=response.status_code,
        message=f"vLLM server가 HTTP {response.status_code}를 반환했습니다: {response.text[:200]}",
    )


def list_models(config: Settings = settings, timeout_seconds: float = 5.0) -> HealthResult:
    endpoint = f"{config.vllm_base_url.rstrip('/')}/models"
    try:
        response = requests.get(
            endpoint,
            headers={"Authorization": f"Bearer {config.vllm_api_key}"},
            timeout=timeout_seconds,
        )
    except requests.RequestException as exc:
        return HealthResult(
            ok=False,
            endpoint=endpoint,
            status_code=None,
            message=f"/v1/models를 읽을 수 없습니다: {exc}",
        )

    if response.ok:
        return HealthResult(
            ok=True,
            endpoint=endpoint,
            status_code=response.status_code,
            message=response.text[:500],
        )

    return HealthResult(
        ok=False,
        endpoint=endpoint,
        status_code=response.status_code,
        message=f"/v1/models가 HTTP {response.status_code}를 반환했습니다: {response.text[:200]}",
    )
