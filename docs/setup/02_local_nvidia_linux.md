# Local NVIDIA Linux 환경

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

Linux에서 NVIDIA GPU로 vLLM을 로컬 실행하려는 경우 읽습니다.

## 준비

```bash
uv sync --extra dev
cp .env.example .env
```

vLLM 설치는 환경에 따라 달라질 수 있습니다. 현재 환경에서 가능하다면 다음 extra를 사용할 수 있습니다.

```bash
uv sync --extra serve
```

## 실행

서버 명령을 출력합니다.

```bash
uv run python scripts/local_serve_help.py
```

출력된 `vllm serve ...` 명령을 첫 번째 터미널에서 실행합니다.

두 번째 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

## 자주 막히는 지점

모델이 메모리에 올라가지 않으면 `.env`에서 다음 값을 사용하세요.

```env
MODEL_PROFILE=tiny
DEFAULT_MAX_MODEL_LEN=2048
```

## 다음 문서

[실습 1: vLLM을 왜 쓰나요?](../labs/01_why_vllm.md)
