# Docker smoke test

Docker는 선택 경로입니다. 기본 학습 경로는 local `vllm serve`입니다.

이 문서는 Docker로 vLLM OpenAI-compatible server를 한 번 실행하고, 같은 Python client로 호출되는지만 확인합니다.

Apple Silicon + Colima 환경에서는 다음 `.env` 값을 권장합니다.

```env
DOCKER_IMAGE=vllm/vllm-openai-cpu:latest-arm64
MODEL_DEFAULT=Qwen/Qwen2.5-0.5B-Instruct
DEFAULT_DTYPE=float32
DEFAULT_MAX_MODEL_LEN=512
DOCKER_CPU_KVCACHE_SPACE=1
```

Colima memory가 2GiB 수준이면 모델 로딩 중 종료될 수 있습니다.

```bash
colima stop
colima start --cpu 4 --memory 8
```

## 시작

```bash
cp .env.example .env
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

model에 Hugging Face 접근 권한이 필요하면 local `.env`에만 `HF_TOKEN`을 설정하세요. 실제 token은 commit하지 않습니다.
