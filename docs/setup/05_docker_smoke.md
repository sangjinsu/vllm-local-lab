# Docker smoke test 준비

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

Docker로 vLLM server를 한 번 띄우고 같은 Python client로 호출되는지만 확인하고 싶을 때 읽습니다.

Docker는 선택 경로입니다. 기본 학습 경로는 local `vllm serve`입니다.

## 실행

```bash
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

## 다음 문서

[실습 9: Docker smoke test](../labs/09_docker_smoke.md)
