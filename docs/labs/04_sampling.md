# 실습 4: Sampling 설정 바꾸기

[전체 목차](../README.md) | 이전: [실습 3](03_first_python_client.md) | 다음: [실습 5](05_local_benchmark.md)

## 이번 챕터 목표

`temperature`, `top_p`, `max_tokens`를 바꾸며 출력 차이를 관찰합니다.

## 예상 시간

10분

## 시작 전 확인

local vLLM server가 실행 중이어야 합니다.

## 실행

`.env`에서 기본 sampling 값을 확인합니다.

```env
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9
DEFAULT_MAX_TOKENS=256
```

sampling test를 실행합니다.

```bash
uv run python scripts/run_sampling_test.py
```

## 성공 확인

여러 sampling 설정의 출력이 순서대로 표시되면 성공입니다.

## 실험해 보기

더 안정적인 출력을 보고 싶다면 다음처럼 낮춰 봅니다.

```env
DEFAULT_TEMPERATURE=0.2
```

request sampling 값은 client 요청에 들어가므로 server를 다시 시작하지 않아도 됩니다.

## 다음 챕터

[실습 5: 로컬 benchmark](05_local_benchmark.md)
