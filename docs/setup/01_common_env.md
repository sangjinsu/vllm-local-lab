# 공통 `.env` 설정

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

모든 실습 전에 읽습니다. 이 프로젝트의 공통 설정은 `.env`에서 관리합니다.

## 만들기

```bash
cp .env.example .env
```

## 처음 확인할 값

```env
MODEL_PROFILE=tiny
VLLM_BASE_URL=http://localhost:8000/v1
VLLM_API_KEY=EMPTY
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9
DEFAULT_MAX_TOKENS=256
```

## 서버 명령 확인

```bash
uv run python scripts/local_serve_help.py
```

출력된 명령을 복사해 vLLM server를 시작합니다.

## 주의

`.env`에는 local 설정과 token이 들어갈 수 있습니다. commit하지 마세요.

## 다음 문서

내 환경에 맞는 setup 문서를 읽은 뒤 [실습 1](../labs/01_why_vllm.md)로 이동하세요.
