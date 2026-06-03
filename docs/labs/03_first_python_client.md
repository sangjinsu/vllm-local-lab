# 실습 3: 첫 Python client 호출

[전체 목차](../README.md) | 이전: [실습 2](02_local_first_server.md) | 다음: [실습 4](04_sampling.md)

## 이번 챕터 목표

local vLLM server를 Python에서 OpenAI-compatible client로 호출합니다.

## 예상 시간

10분

## 시작 전 확인

실습 2의 `vllm serve ...` 명령이 실행 중이어야 합니다.

## 실행

```bash
uv run python scripts/call_chat.py
```

이 script는 내부적으로 다음 구조를 사용합니다.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
)
```

프로젝트 코드에서는 이 설정을 직접 쓰지 않고 `vllm_lab.client.create_client()`를 통해 `.env` 값을 사용합니다.

## 성공 확인

터미널에 local model의 짧은 답변이 출력되면 성공입니다.

## 자주 막히는 지점

`Connection error`가 나오면 server가 켜져 있는지 확인하고 다음 명령으로 다시 server 명령을 확인하세요.

```bash
uv run python scripts/local_serve_help.py
```

`400 Bad Request`와 함께 `maximum context length` 오류가 나오면 `.env`의 출력 token을 낮추세요.

```env
DEFAULT_MAX_TOKENS=32
```

`max-model-len`은 입력 prompt와 출력 token을 합친 한도입니다. 작은 context로 server를 띄운 경우 `DEFAULT_MAX_TOKENS=256`은 너무 클 수 있습니다.

## 다음 챕터

[실습 4: Sampling 설정 바꾸기](04_sampling.md)
