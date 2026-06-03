# 문제 해결

[문서 목차로 돌아가기](../README.md)

## client가 연결되지 않을 때

먼저 server 명령을 확인합니다.

```bash
uv run python scripts/local_serve_help.py
```

출력된 `vllm serve ...` 명령을 실행한 뒤 다시 확인합니다.

```bash
uv run python scripts/healthcheck.py
```

## 모델이 메모리에 올라가지 않을 때

작은 profile을 사용합니다.

```env
MODEL_PROFILE=tiny
DEFAULT_MAX_MODEL_LEN=2048
```

`.env`를 바꾼 뒤에는 vLLM server를 다시 시작하세요.

## Hugging Face 접근이 실패할 때

일부 선택 모델은 Hugging Face 접근 권한이 필요할 수 있습니다.

local `.env`에만 `HF_TOKEN`을 설정하세요. 실제 token은 commit하지 않습니다.

## benchmark가 너무 오래 걸릴 때

작은 값부터 시작합니다.

```env
BENCHMARK_NUM_PROMPTS=5
BENCHMARK_REQUEST_RATE=1
BENCHMARK_MAX_TOKENS_LIST=64
```

## 다음 문서

문제가 해결되면 [문서 목차](../README.md)에서 진행하던 챕터로 돌아가세요.
