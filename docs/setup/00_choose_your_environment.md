# 환경 선택

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

처음 시작할 때 내 환경에서 어떤 순서로 진행할지 정하기 위해 읽습니다.

이 프로젝트의 기본 경로는 local `vllm serve`입니다. Docker와 Kubernetes는 선택 smoke test입니다.

## 추천 경로

| 환경 | 읽을 문서 |
|---|---|
| Linux + NVIDIA GPU | [Local NVIDIA Linux](02_local_nvidia_linux.md) |
| Windows + WSL + NVIDIA GPU | [Windows NVIDIA WSL](03_windows_nvidia_wsl.md) |
| Apple Silicon macOS | [Apple Silicon](04_apple_silicon.md) |
| Docker로 서버 실행만 확인 | [Docker smoke test](05_docker_smoke.md) |
| kind로 로컬 Kubernetes 확인 | [Kubernetes kind smoke test](06_kubernetes_kind_smoke.md) |

## 모든 환경에서 먼저 할 일

```bash
uv sync --extra dev
cp .env.example .env
```

처음 성공을 빠르게 확인하려면 `.env`에서 다음 값을 권장합니다.

```env
MODEL_PROFILE=tiny
```

## 다음 문서

[공통 `.env` 설정](01_common_env.md)을 읽고 설정값의 의미를 확인하세요.
