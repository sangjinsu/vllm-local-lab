# 2026-06-10 Windows NVIDIA WSL smoke test 기록

[문서 목차로 돌아가기](../README.md)

이 문서는 이 프로젝트를 실제 Windows + NVIDIA GPU + WSL2 Ubuntu 환경에서 로컬 학습 경로(챕터 1~8)로 진행하며 확인한 테스트 기록입니다.

같은 날 작성된 [readiness 리뷰](2026-06-10_nvidia_wsl_readiness.md)는 WSL2 Ubuntu 미설치로 런타임 검증이 막혀 있었습니다. 이번 기록은 그 블로커가 해소된 뒤 실제로 vLLM server를 띄워 챕터를 실행한 결과입니다.

이 결과는 절대 성능 기준이 아닙니다. 같은 모델이라도 vLLM 버전, GPU, driver, WSL 설정, 실행 중인 다른 process에 따라 latency와 throughput은 달라집니다.

## 환경

| 항목 | 값 |
|---|---|
| Host | Windows 11 + WSL2 Ubuntu 24.04.3 LTS |
| GPU | NVIDIA GeForce RTX 5060 (Blackwell, sm_120) |
| Driver / CUDA(driver 보고) | 591.74 / 13.1 |
| VRAM | 8151 MiB total (Windows가 상시 약 0.9~1.1 GiB 사용) |
| WSL 내부 `nvidia-smi` | 정상 (GPU passthrough 동작) |
| 실행 위치 | `~/vllm-local-lab` (WSL Linux 파일시스템에 clone) |
| Python | `uv` 관리 환경 |
| vLLM | `0.22.0` |
| torch | `2.11.0+cu130` (CUDA 13 빌드, sm_120 지원) |
| 주요 model | `Qwen/Qwen2.5-0.5B-Instruct` |
| Model profile | `tiny` |
| max-model-len | `2048` |
| 기본 max tokens | `64` |
| Benchmark | `num_prompts=5`, `request_rate=1`, `prompt_preset=short` |

이번 환경에서 server를 안정적으로 띄우기 위해 필요했던 옵션:

```bash
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 --port 8000 \
  --dtype auto --max-model-len 2048 \
  --gpu-memory-utilization 0.80 \
  --enforce-eager
```

## 진행한 테스트

| 챕터 | 확인한 내용 | 결과 |
|---|---|---|
| 1. Why vLLM | 개념 문서 | 해당 없음 (코드 실행 아님) |
| 사전: 단위 테스트 | `uv run pytest -q` | `12 passed` |
| 2. Local server | `local_serve_help.py` → `vllm serve` → `/health`, `/v1/models` | 성공 (모델이 `Qwen/Qwen2.5-0.5B-Instruct`로 올바르게 보고됨) |
| 3. Python client | `call_chat.py`, `call_completion.py` | 성공 (정상 응답) |
| 4. Sampling | `run_sampling_test.py` (temperature/top_p 변경) | 출력 차이 확인 |
| 5. Benchmark | `run_benchmark.py` | `results/benchmarks/latest.{csv,md}` 생성 |
| 6. Prefix caching | `--enable-prefix-caching` on/off benchmark 비교 | 동작 확인 (이번 run에서는 off가 더 빠름) |
| 7. LoRA serving | placeholder adapter로 구조 검증 + `local_serve_help.py` LoRA 옵션 출력 | 성공 (구조 검증 통과, placeholder 경고) |
| 8. Speculative decoding | ngram speculative server 재기동 후 benchmark 비교 | 동작 확인 (이번 run에서는 baseline이 더 빠름) |

> Docker(챕터 9), Kubernetes kind(챕터 10)는 이번 검증 범위에서 제외했습니다.

## Benchmark 결과

| 구분 | Prefix Cache | Speculative | Avg Latency | Throughput | Completed |
|---|---|---|---:|---:|---:|
| Baseline | `false` | 없음 | `0.547s` | `98.29 tok/s` | `5` |
| Prefix caching 비교 | `true` | 없음 | `0.690s` | `64.64 tok/s` | `5` |
| Speculative 비교 | `false` | `ngram` | `0.954s` | `50.73 tok/s` | `5` |

ngram speculative config: `{"method":"ngram","num_speculative_tokens":3,"prompt_lookup_min":2,"prompt_lookup_max":5}`

## 해석

- 챕터 1~8의 로컬 학습 경로가 Windows NVIDIA GPU(WSL2) 환경에서 정상 동작함을 확인했습니다.
- 실 GPU라 같은 tiny 모델 기준 Apple Silicon CPU run(약 1.3s, 12 tok/s)보다 훨씬 빨랐습니다(baseline 0.547s, 98 tok/s).
- 이번 작은 benchmark에서는 prefix caching과 speculative decoding이 더 빠르지 않았습니다. 짧고 서로 다른 프롬프트라 공유 prefix·반복 n-gram이 거의 없어 부가 오버헤드가 더 컸기 때문이며, 문서에서 설명한 정상 범위입니다.
- readiness 리뷰에서 `/v1/models`가 7B 모델을 잘못 보고했던 문제는, 이번에 의도한 tiny 모델 server를 직접 띄우면서 해소됐습니다.

## 테스트 중 확인한 주의점 (Windows NVIDIA WSL 고유)

- **FlashInfer 샘플러는 `nvcc`가 필요합니다.** pip wheel로 받은 CUDA 런타임만으로는 FlashInfer가 top-k/top-p 커널을 JIT 컴파일하지 못해 server가 모델 로딩 직후 멈춥니다(`Could not find nvcc and default cuda_home='/usr/local/cuda' doesn't exist`). `VLLM_USE_FLASHINFER_SAMPLER=0`으로 네이티브 sampler 경로를 사용하면 정상 기동합니다. CUDA Toolkit(nvcc)을 WSL에 설치하는 것도 대안입니다.
- **8GB GPU에서는 `--gpu-memory-utilization`을 낮춰야 합니다.** Windows가 GPU를 상시 약 1GB 사용하므로 vLLM 기본값 `0.92`(약 7.32 GiB 요구)는 가용 메모리 부족으로 실패합니다(`Free memory ... is less than desired GPU memory utilization`). `0.80` 정도로 낮추면 안정적입니다. `scripts/local_serve_help.py`가 생성하는 명령에는 이 옵션이 없으므로 수동으로 덧붙여야 합니다.
- **`--enforce-eager` 권장.** WSL에서 `torch.compile`/cudagraph 캡처 단계가 매우 느려, smoke test에서는 `--enforce-eager`로 건너뛰면 기동이 빠릅니다(약 15~20초).
- WSL에서는 `pin_memory=False`로 동작한다는 경고가 나오며 약간의 성능 저하가 있을 수 있습니다.
- `--speculative-config` 값은 shell에서 한 줄 JSON 문자열로 넘겨야 합니다.

## 다음에 비교해 볼 것

- `VLLM_USE_FLASHINFER_SAMPLER=0` 대신 WSL에 CUDA Toolkit(nvcc)을 설치해 FlashInfer 경로를 살린 뒤 성능 비교
- compile(`--enforce-eager` 제거) 기동이 WSL에서 실제로 완료되는지, 완료 시 throughput 변화
- `BENCHMARK_NUM_PROMPTS`를 늘리고 공유 prefix가 큰 프롬프트로 prefix caching 효과 재확인
- Docker(챕터 9), kind(챕터 10) GPU smoke test로 범위 확장
