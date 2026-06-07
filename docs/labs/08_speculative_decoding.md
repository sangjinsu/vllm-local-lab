# 실습 8: Speculative decoding

[전체 목차](../README.md) | 이전: [실습 7](07_lora_serving.md) | 다음: [실습 9](09_docker_smoke.md)

## 이번 챕터 목표

baseline 설정과 speculative decoding 설정을 benchmark로 비교합니다.

speculative decoding은 항상 성능을 개선하지 않습니다. workload와 model 조합에 따라 결과가 달라질 수 있습니다.

## 예상 시간

15분

## 시작 전 확인

사용할 speculative config를 정해야 합니다.

## 실행

`.env`를 설정합니다.

```env
ENABLE_SPECULATIVE_DECODING=true
SPECULATIVE_CONFIG_JSON={"model":"Qwen/Qwen2.5-0.5B-Instruct","num_speculative_tokens":4}
```

Apple Silicon CPU 환경에서 ngram 방식만 가볍게 확인할 때는 다음처럼 더 작은 설정부터 시작할 수 있습니다.

```env
DEFAULT_TEMPERATURE=0
DEFAULT_TOP_P=1.0
SPECULATIVE_CONFIG_JSON={"method":"ngram","num_speculative_tokens":1,"prompt_lookup_min":2,"prompt_lookup_max":5}
```

설정을 확인합니다.

```bash
uv run python scripts/run_speculative_test.py
```

vLLM server를 speculative config와 함께 다시 시작한 뒤 benchmark를 실행합니다.

```bash
uv run python scripts/run_benchmark.py
```

## 성공 확인

baseline run과 speculative run의 `latest.md` 결과를 비교할 수 있으면 성공입니다.

## 이번 테스트에서 배운 점

이번 Apple Silicon CPU run에서는 speculative decoding이 baseline보다 빠르지 않았습니다.

| 설정 | Avg Latency | Throughput |
|---|---:|---:|
| Speculative | `1.534748s` | `10.425163 tok/s` |
| Baseline | `1.328743s` | `12.041458 tok/s` |

speculative decoding은 workload, model, sampling 설정, backend에 따라 결과가 달라집니다.

## 자주 막히는 지점

속도가 항상 좋아진다고 가정하지 마세요. 비교 결과가 나빠질 수도 있습니다.

`--speculative-config`를 shell에서 줄바꿈하면 `expected one argument` 오류가 납니다. JSON 값은 한 줄 문자열로 넘기세요.

## 다음 챕터

[실습 9: Docker smoke test](09_docker_smoke.md)
