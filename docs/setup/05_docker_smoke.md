# Docker smoke test 준비

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

Docker로 vLLM server를 한 번 띄우고 같은 Python client로 호출되는지만 확인하고 싶을 때 읽습니다.

Docker는 선택 경로입니다. 기본 학습 경로는 local `vllm serve`입니다.

## Apple Silicon + Colima

Apple Silicon에서 Colima를 사용한다면 먼저 Docker VM resource를 확인합니다.

```bash
colima list
docker info --format 'CPUs={{.NCPU}} Mem={{.MemTotal}} Arch={{.Architecture}}'
```

memory가 2GiB 수준이면 vLLM CPU image가 모델 로딩 중 종료될 수 있습니다. smoke test 전에는 다음처럼 늘립니다.

```bash
colima stop
colima start --cpu 4 --memory 8
```

`.env`에는 CPU image와 작은 model 설정을 사용합니다.

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

## 다음 문서

[실습 9: Docker smoke test](../labs/09_docker_smoke.md)
