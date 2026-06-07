# 실습 4: Sampling 설정 바꾸기

[전체 목차](../README.md) | 이전: [실습 3](03_first_python_client.md) | 다음: [실습 5](05_local_benchmark.md)

## 이번 챕터 목표

`temperature`, `top_p`, `max_tokens`를 바꾸며 출력 차이를 관찰합니다.

## 예상 시간

10분

## 시작 전 확인

local vLLM server가 실행 중이어야 합니다.

Apple Silicon CPU backend처럼 작은 context로 server를 띄운 경우 `.env`에서 출력 token을 먼저 낮춰 둡니다.

```env
DEFAULT_MAX_TOKENS=32
```

## 실행

`.env`에서 기본 sampling 값을 확인합니다.

```env
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9
DEFAULT_MAX_TOKENS=32
```

sampling test를 실행합니다.

```bash
uv run python scripts/run_sampling_test.py
```

## 성공 확인

여러 sampling 설정의 출력이 순서대로 표시되면 성공입니다.

이 챕터의 성공 기준은 정답성이 아니라 출력 다양성입니다. 작은 model은 다음처럼 `vLLM`을 잘못 풀이할 수 있습니다.

```text
Virtual Local Language Model
Vector-Length Model
Vocabulary-Limited Language Model
```

이런 hallucination이 나와도 sampling request 자체가 실패한 것은 아닙니다. 지금은 `temperature`와 `top_p` 값이 request마다 다르게 들어가고, 출력이 달라지는지 확인합니다.

## 실험해 보기

더 안정적인 출력을 보고 싶다면 다음처럼 낮춰 봅니다.

```env
DEFAULT_TEMPERATURE=0.2
```

request sampling 값은 client 요청에 들어가므로 server를 다시 시작하지 않아도 됩니다.

답변 정확도를 조금 더 높이고 싶다면 prompt에 짧은 배경 정보를 넣어 비교해 보세요.

```text
vLLM is an LLM serving engine. Write one practical reason to run a local vLLM server.
```

답변이 계속 틀리면 [문제 해결: 답변 내용이 틀릴 때](../setup/07_troubleshooting.md#답변-내용이-틀릴-때)를 확인하세요.

## 더 깊이 이해하기

각 sampling 파라미터의 의미와 출력 형식 강제(guided decoding)는 다음 심화 문서에서 다룹니다.

- [심화 10: Sampling과 guided decoding](../deep-dive/10_sampling_and_guided_decoding.md)

## 다음 챕터

[실습 5: 로컬 benchmark](05_local_benchmark.md)
