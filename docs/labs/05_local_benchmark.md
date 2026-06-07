# 실습 5: 로컬 benchmark

[전체 목차](../README.md) | 이전: [실습 4](04_sampling.md) | 다음: [실습 6](06_prefix_caching.md)

## 이번 챕터 목표

local vLLM server를 간단히 benchmark하고, `.env` 값을 바꾸며 결과를 비교합니다.

## 예상 시간

15분

## 시작 전 확인

local vLLM server가 실행 중이어야 합니다.

처음에는 작은 benchmark 설정을 권장합니다.

```env
BENCHMARK_NUM_PROMPTS=5
BENCHMARK_REQUEST_RATE=1
BENCHMARK_PROMPT_PRESET=short
DEFAULT_MAX_TOKENS=64
```

## 실행

단일 benchmark:

```bash
uv run python scripts/run_benchmark.py
```

matrix benchmark:

```bash
uv run python scripts/run_benchmark_matrix.py
```

## 성공 확인

다음 파일이 생성되면 성공입니다.

```text
results/benchmarks/latest.csv
results/benchmarks/latest.md
```

## 비교해 볼 값

- `MODEL_PROFILE`
- `DEFAULT_MAX_TOKENS`
- `BENCHMARK_PROMPT_PRESET`
- `BENCHMARK_REQUEST_RATE`
- `ENABLE_PREFIX_CACHING`

## 자주 막히는 지점

benchmark가 오래 걸리면 `BENCHMARK_NUM_PROMPTS`와 `BENCHMARK_REQUEST_RATE`를 낮추세요.

## 더 깊이 이해하기

benchmark 숫자의 의미와 튜닝 원리는 다음 심화 문서에서 다룹니다.

- [심화 1: 추론 성능 지표](../deep-dive/01_inference_metrics.md)
- [심화 3: 배치와 스케줄링](../deep-dive/03_batching_and_scheduling.md)

## 다음 챕터

[실습 6: Prefix caching](06_prefix_caching.md)
