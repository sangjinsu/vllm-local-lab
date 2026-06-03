# 실습 2: 로컬 vLLM 서버 실행

[전체 목차](../README.md) | 이전: [실습 1](01_why_vllm.md) | 다음: [실습 3](03_first_python_client.md)

## 이번 챕터 목표

`.env` 값을 기준으로 첫 local vLLM server를 실행합니다.

## 예상 시간

10분

## 시작 전 확인

`.env`가 없다면 먼저 만듭니다.

```bash
cp .env.example .env
```

처음 실행은 작은 model profile을 권장합니다.

```env
MODEL_PROFILE=tiny
```

## 실행

server 명령을 출력합니다.

```bash
uv run python scripts/local_serve_help.py
```

출력은 다음과 비슷합니다.

```bash
vllm serve Qwen/Qwen3-0.6B \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype auto \
  --max-model-len 4096
```

출력된 명령을 첫 번째 터미널에서 실행합니다.

Apple Silicon macOS에서 CPU backend로 실행 중이라면 일반 helper 명령보다 [Apple Silicon 환경](../setup/04_apple_silicon.md)의 `Mac CPU 권장 server 명령`을 먼저 사용하세요. `--enforce-eager`, `--dtype float32`, 작은 `--max-model-len`이 필요할 수 있습니다.

## 성공 확인

두 번째 터미널에서 health check를 실행합니다.

```bash
uv run python scripts/healthcheck.py
```

server가 켜져 있으면 `/health`와 `/v1/models` 확인 결과가 출력됩니다.

## 자주 막히는 지점

- 연결이 실패하면 server 터미널이 아직 실행 중인지 확인하세요.
- 모델이 너무 크면 `MODEL_PROFILE=tiny`와 `DEFAULT_MAX_MODEL_LEN=2048`로 낮춰 보세요.
- `.env`를 바꾼 뒤에는 server를 다시 시작해야 합니다.
- Apple Silicon에서 `No available shared memory broadcast block found`가 반복되면 [문제 해결](../setup/07_troubleshooting.md)을 확인하세요.

## 다음 챕터

[실습 3: 첫 Python client 호출](03_first_python_client.md)
