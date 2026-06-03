# Benchmark 보고서 템플릿

[전체 목차](../README.md) | 관련 챕터: [실습 5](05_local_benchmark.md)

benchmark 결과를 직접 정리하고 싶을 때 이 표를 사용합니다.

| Model Profile | Max Tokens | Prompt Preset | Request Rate | Prefix Cache | Avg Latency | Throughput | Notes |
|---|---:|---|---:|---|---:|---:|---|
| tiny | 64 | short | 1 | false |  |  |  |
| tiny | 128 | short | 1 | false |  |  |  |
| default | 128 | medium | 2 | true |  |  |  |

## 지표 읽는 법

`Avg Latency`는 request 하나가 평균적으로 걸린 시간입니다.

`Throughput`은 초당 생성 token 수입니다.

이 숫자는 내 로컬 환경에서 설정을 비교하기 위한 값입니다. 모든 환경에 일반화되는 성능 수치로 해석하지 마세요.
