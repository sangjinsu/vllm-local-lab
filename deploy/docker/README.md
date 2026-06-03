# Docker smoke test

Docker는 선택 경로입니다. 기본 학습 경로는 local `vllm serve`입니다.

이 문서는 Docker로 vLLM OpenAI-compatible server를 한 번 실행하고, 같은 Python client로 호출되는지만 확인합니다.

## 시작

```bash
cp .env.example .env
docker compose -f deploy/docker/docker-compose.yml up
```

다른 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

## 종료

```bash
docker compose -f deploy/docker/docker-compose.yml down
```

model에 Hugging Face 접근 권한이 필요하면 local `.env`에만 `HF_TOKEN`을 설정하세요. 실제 token은 commit하지 않습니다.
