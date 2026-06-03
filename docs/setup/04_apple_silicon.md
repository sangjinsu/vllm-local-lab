# Apple Silicon 환경

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

Apple Silicon macOS에서 가능한 범위의 로컬 실습을 확인하려는 경우 읽습니다.

## 준비

```bash
uv sync --extra dev
cp .env.example .env
```

처음에는 작은 설정을 권장합니다.

```env
MODEL_PROFILE=tiny
DEFAULT_DTYPE=auto
DEFAULT_MAX_MODEL_LEN=2048
```

## 실행

```bash
uv run python scripts/local_serve_help.py
```

출력된 명령을 기준으로 현재 vLLM 설치 환경에서 가능한지 확인합니다.

## 자주 막히는 지점

Apple Silicon의 vLLM 지원과 성능은 설치 방식과 vLLM 버전에 따라 달라질 수 있습니다. 이 경우에도 Python client, `.env`, benchmark 구조는 그대로 학습할 수 있습니다.

Docker와 Kubernetes는 여전히 선택 smoke test이며 기본 학습 경로가 아닙니다.

## 다음 문서

[실습 1: vLLM을 왜 쓰나요?](../labs/01_why_vllm.md)
