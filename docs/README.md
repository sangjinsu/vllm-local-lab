# vLLM Local Lab 문서 목차

이 문서는 학습자가 챕터별로 쉽게 이동할 수 있도록 만든 시작점입니다.

처음이라면 `환경 준비 → 실습 1 → 실습 2 → 실습 3` 순서로 진행하세요. Docker와 Kubernetes는 나중에 선택적으로 확인합니다.

## 1. 환경 준비

| 순서 | 문서 | 언제 읽나요? |
|---:|---|---|
| 0 | [환경 선택](setup/00_choose_your_environment.md) | 내 환경에서 어떤 경로로 시작할지 정할 때 |
| 1 | [공통 `.env` 설정](setup/01_common_env.md) | 모든 실습 전에 반드시 |
| 2 | [Local NVIDIA Linux](setup/02_local_nvidia_linux.md) | Linux + NVIDIA GPU 환경 |
| 3 | [Windows NVIDIA WSL](setup/03_windows_nvidia_wsl.md) | Windows WSL 환경 |
| 4 | [Apple Silicon](setup/04_apple_silicon.md) | macOS Apple Silicon 환경 |
| 5 | [Docker smoke test](setup/05_docker_smoke.md) | Docker로 서버 실행만 확인할 때 |
| 6 | [Kubernetes kind smoke test](setup/06_kubernetes_kind_smoke.md) | kind로 로컬 Kubernetes 확인할 때 |
| 7 | [문제 해결](setup/07_troubleshooting.md) | 연결 실패, 모델 메모리 문제, token 문제를 볼 때 |

## 2. 실습 챕터

각 챕터는 `목표 → 준비 → 실행 → 확인 → 다음 챕터` 순서로 구성되어 있습니다.

| 순서 | 문서 | 결과 |
|---:|---|---|
| 1 | [vLLM을 왜 쓰나요?](labs/01_why_vllm.md) | 전체 학습 흐름 이해 |
| 2 | [로컬 vLLM 서버 실행](labs/02_local_first_server.md) | `vllm serve` 실행 |
| 3 | [첫 Python client 호출](labs/03_first_python_client.md) | OpenAI-compatible API 호출 |
| 4 | [Sampling 설정 바꾸기](labs/04_sampling.md) | `temperature`, `top_p`, `max_tokens` 비교 |
| 5 | [로컬 benchmark](labs/05_local_benchmark.md) | latency와 throughput 보고서 생성 |
| 6 | [Prefix caching](labs/06_prefix_caching.md) | 반복 prompt 실험 |
| 7 | [LoRA serving](labs/07_lora_serving.md) | 기존 LoRA adapter 설정 확인 |
| 8 | [Speculative decoding](labs/08_speculative_decoding.md) | baseline과 speculative 설정 비교 |
| 9 | [Docker smoke test](labs/09_docker_smoke.md) | Docker 서버와 같은 Python client 확인 |
| 10 | [Kubernetes kind smoke test](labs/10_kubernetes_kind_smoke.md) | kind 서버와 같은 Python client 확인 |

## 3. 부록

부록은 실습을 먼저 진행한 뒤 필요한 개념만 골라 읽어도 됩니다.

| 문서 | 다루는 개념 |
|---|---|
| [LLM 기본](appendix/01_llm_basics.md) | prompt와 token |
| [Transformer attention](appendix/02_transformer_attention.md) | attention의 직관 |
| [Prefill과 decode](appendix/03_prefill_decode.md) | serving 단계 |
| [KV cache](appendix/04_kv_cache.md) | cache가 필요한 이유 |
| [Batching](appendix/05_batching.md) | 여러 요청 처리 |
| [Quantization](appendix/06_quantization.md) | 메모리 사용 줄이기 |
| [LoRA와 QLoRA](appendix/07_lora_qlora.md) | adapter serving의 배경 |
| [Mermaid 요약](appendix/08_mermaid_summary.md) | 전체 흐름 그림 |

## 4. 막혔을 때

가장 먼저 다음 순서로 확인하세요.

```bash
uv run python scripts/local_serve_help.py
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

그래도 해결되지 않으면 [문제 해결](setup/07_troubleshooting.md)을 확인합니다.
