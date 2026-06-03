# 실습 9: Docker smoke test

[전체 목차](../README.md) | 이전: [실습 8](08_speculative_decoding.md) | 다음: [실습 10](10_kubernetes_kind_smoke.md)

## 이번 챕터 목표

Docker로 vLLM server를 한 번 실행하고, 같은 Python client로 호출되는지 확인합니다.

Docker는 선택 smoke test입니다. 기본 학습 경로는 local `vllm serve`입니다.

## 예상 시간

10분

## 시작 전 확인

Docker가 실행 가능한 환경이어야 합니다.

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

## 성공 확인

local server 때와 같은 Python client가 Docker server에도 연결되면 성공입니다.

## 다음 챕터

[실습 10: Kubernetes kind smoke test](10_kubernetes_kind_smoke.md)
