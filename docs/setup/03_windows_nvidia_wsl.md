# Windows NVIDIA WSL 환경

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

Windows에서 WSL을 사용하고 NVIDIA GPU를 연결해 실습하려는 경우 읽습니다.

## 준비

WSL 안에서 실행합니다.

```bash
uv sync --extra dev
cp .env.example .env
```

처음에는 작은 모델을 권장합니다.

```env
MODEL_PROFILE=tiny
```

## 실행

```bash
uv run python scripts/local_serve_help.py
```

출력된 `vllm serve ...` 명령을 실행한 뒤, 다른 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

## 자주 막히는 지점

client가 연결되지 않으면 `VLLM_PORT`와 server가 실제로 listening 중인 port가 같은지 확인하세요.

## 다음 문서

[실습 1: vLLM을 왜 쓰나요?](../labs/01_why_vllm.md)
