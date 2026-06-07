# 실습 9: Docker smoke test

[전체 목차](../README.md) | 이전: [실습 8](08_speculative_decoding.md) | 다음: [실습 10](10_kubernetes_kind_smoke.md)

## 이번 챕터 목표

Docker로 vLLM server를 한 번 실행하고, 같은 Python client로 호출되는지 확인합니다.

Docker는 선택 smoke test입니다. 기본 학습 경로는 local `vllm serve`입니다.

## 예상 시간

10분

## 시작 전 확인

Docker가 실행 가능한 환경이어야 합니다.

Apple Silicon에서 Colima를 사용한다면 Docker VM memory를 8GiB 정도로 둡니다.

```bash
colima stop
colima start --cpu 4 --memory 8
```

`.env`에는 ARM CPU image와 작은 모델 설정을 사용합니다.

```env
DOCKER_IMAGE=vllm/vllm-openai-cpu:latest-arm64
MODEL_DEFAULT=Qwen/Qwen2.5-0.5B-Instruct
DEFAULT_DTYPE=float32
DEFAULT_MAX_MODEL_LEN=512
DOCKER_CPU_KVCACHE_SPACE=1
```

## 실행

```bash
docker compose --env-file .env -f deploy/docker/docker-compose.yml up
```

다른 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

## 종료

```bash
docker compose --env-file .env -f deploy/docker/docker-compose.yml down
```

## 성공 확인

local server 때와 같은 Python client가 Docker server에도 연결되면 성공입니다.

## 자주 막히는 지점

- `Failed to infer device type`이 나오면 GPU image를 CPU-only Docker 환경에서 실행한 것입니다. Apple Silicon에서는 `DOCKER_IMAGE=vllm/vllm-openai-cpu:latest-arm64`를 사용하세요.
- `OOMKilled=true` 또는 `Exited (137)`이 나오면 Colima memory를 늘리세요.
- KV cache allocation 오류가 나오면 `DOCKER_CPU_KVCACHE_SPACE=1`처럼 CPU KV cache 크기를 명시하세요.

## 다음 챕터

[실습 10: Kubernetes kind smoke test](10_kubernetes_kind_smoke.md)
