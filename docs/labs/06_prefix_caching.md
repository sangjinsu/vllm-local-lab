# 실습 6: Prefix caching

[전체 목차](../README.md) | 이전: [실습 5](05_local_benchmark.md) | 다음: [실습 7](07_lora_serving.md)

## 이번 챕터 목표

반복되는 긴 prompt에서 prefix caching이 어떤 상황에 도움이 되는지 실험합니다.

## 예상 시간

15분

## 시작 전 확인

local vLLM server를 재시작할 수 있어야 합니다.

## 실행

`.env`를 설정합니다.

```env
ENABLE_PREFIX_CACHING=true
BENCHMARK_PROMPT_PRESET=long
```

server 명령을 다시 출력합니다.

```bash
uv run python scripts/local_serve_help.py
```

출력된 명령에 `--enable-prefix-caching`이 포함되는지 확인하고 server를 다시 시작합니다.

benchmark를 실행합니다.

```bash
uv run python scripts/run_benchmark.py
```

## 성공 확인

`results/benchmarks/latest.md`가 생성되고 `Prefix Cache` 값이 `true`로 기록되면 성공입니다.

## 이번 테스트에서 배운 점

Apple Silicon CPU 환경의 작은 benchmark에서는 prefix caching을 켠 run이 더 빠르지 않았습니다.

이번 기록에서는 `prefix_cache=true`가 평균 `2.487104s`, `prefix_cache=false`가 평균 `1.867628s`였습니다. 이 결과는 prefix caching이 쓸모없다는 뜻이 아니라, 반복 prefix가 충분히 길고 request pattern이 맞아야 효과가 보인다는 뜻입니다.

## 비교해 보기

다음 값으로 바꾸고 다시 실행해 비교합니다.

```env
ENABLE_PREFIX_CACHING=false
```

prefix caching은 모든 workload에서 항상 빨라지는 기능이 아닙니다. 반복 prefix가 있을 때 효과를 기대할 수 있습니다.

## 더 깊이 이해하기

이번 결과가 왜 이렇게 나오는지(블록 해시 공유, 효과 조건)는 다음 심화 문서에서 다룹니다.

- [심화 4: Prefix caching 내부 동작](../deep-dive/04_prefix_caching_internals.md)
- 전제 개념: [심화 2: KV cache와 PagedAttention](../deep-dive/02_kv_cache_and_paged_attention.md)

## 다음 챕터

[실습 7: LoRA serving](07_lora_serving.md)
