# 2026-06-07 Apple Silicon smoke test 기록

[문서 목차로 돌아가기](../README.md)

이 문서는 이 프로젝트를 실제 Apple Silicon macOS 환경에서 진행하며 확인한 테스트 기록입니다.

이 결과는 절대 성능 기준이 아닙니다. 같은 모델이라도 vLLM 버전, CPU/GPU, memory, Colima 설정, 실행 중인 다른 process에 따라 latency와 throughput은 달라집니다.

## 환경

| 항목 | 값 |
|---|---|
| Host | macOS Apple Silicon |
| Local vLLM | source build CPU backend |
| Docker runtime | Colima |
| Colima 설정 | 4 CPU, 8GiB memory |
| Docker image | `vllm/vllm-openai-cpu:latest-arm64` |
| 주요 model | `Qwen/Qwen2.5-0.5B-Instruct` |
| Model profile | `tiny` |
| Benchmark prompt | `long` |
| Benchmark request rate | `1.0` |
| Benchmark completed requests | `3` |
| 기본 max tokens | `16` |

## 진행한 테스트

| 단계 | 확인한 내용 | 결과 |
|---|---|---|
| Local server | `vllm serve`로 server 시작 | 성공 |
| Health check | `/health`, `/v1/models` 호출 | 성공 |
| Python client | `scripts/call_chat.py` 호출 | 성공 |
| Sampling | `temperature`, `top_p` 변경 | 출력 차이 확인 |
| Benchmark | `scripts/run_benchmark.py` 실행 | CSV/Markdown 생성 |
| Prefix caching | `true`, `false` 비교 | CPU 환경에서는 이번 run에서 `false`가 더 빠름 |
| LoRA | adapter path와 필수 파일 확인 | placeholder는 구조 학습용으로 확인 |
| Speculative decoding | baseline과 speculative 비교 | 이번 run에서는 baseline이 더 빠름 |
| Docker smoke | Docker container에서 같은 Python client 호출 | 성공 |
| Kubernetes kind smoke | kind Pod와 Service를 port-forward 후 호출 | 성공 |

## Benchmark 결과

| 구분 | Prefix Cache | Avg Latency | Throughput | Completed |
|---|---|---:|---:|---:|
| Local benchmark 초기값 | `true` | `2.268869s` | `7.051971 tok/s` | `3` |
| Prefix caching 비교 | `true` | `2.487104s` | `6.433185 tok/s` | `3` |
| Prefix caching 비교 | `false` | `1.867628s` | `8.567018 tok/s` | `3` |
| Speculative decoding | `false` | `1.534748s` | `10.425163 tok/s` | `3` |
| Baseline 비교 | `false` | `1.328743s` | `12.041458 tok/s` | `3` |
| Docker smoke | `false` | `1.449252s` | `11.040181 tok/s` | `3` |
| Kubernetes kind smoke | `false` | `1.600385s` | `9.997597 tok/s` | `3` |

## 해석

이번 테스트의 핵심 성공 기준은 성능 최고치를 찾는 것이 아니라, 같은 Python client가 여러 실행 환경에 연결되는지 확인하는 것이었습니다.

- `local`, `Docker`, `kind` 모두 OpenAI-compatible client로 호출할 수 있었습니다.
- Apple Silicon CPU 환경에서는 compile, memory, KV cache 설정을 작게 잡아야 안정적으로 시작됐습니다.
- 이번 작은 benchmark에서는 prefix caching과 speculative decoding이 더 빠르지 않았습니다.
- 작은 model은 연결 확인에는 유용하지만, 답변 품질은 쉽게 흔들릴 수 있습니다.

## 테스트 중 확인한 주의점

- `--speculative-config` 값은 shell에서 한 줄 JSON 문자열로 넘겨야 합니다.
- CPU backend에서는 `--gpu-memory-utilization`이라는 이름의 option도 CPU memory 예약에 영향을 줄 수 있습니다.
- Docker의 기본 GPU image는 Apple Silicon + CPU-only Colima에서 device type 추론에 실패할 수 있습니다.
- kind smoke test에서는 `.env` 전체를 ConfigMap으로 넣지 않고 공개 가능한 설정만 `--from-literal`로 전달합니다.
- `HF_TOKEN`은 local `.env` 또는 Kubernetes Secret에만 두고 문서나 ConfigMap에 넣지 않습니다.

## 다음에 비교해 볼 것

- `BENCHMARK_NUM_PROMPTS`를 늘려 noise를 줄이기
- `prompt_preset=short`, `medium`, `long`을 같은 조건에서 비교하기
- `DEFAULT_MAX_TOKENS`를 16, 32, 64로 바꿔 decode 길이 영향 보기
- GPU 환경에서 같은 실험을 다시 실행해 CPU 결과와 비교하기
