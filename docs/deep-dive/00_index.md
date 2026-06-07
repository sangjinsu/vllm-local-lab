# 심화 학습 (deep-dive) 목차

[문서 목차로 돌아가기](../README.md)

## 이 섹션은 무엇인가요?

`labs/`가 "vLLM을 일단 돌려보기"라면, `appendix/`는 "개념을 한 문장으로 이해하기"입니다.
이 deep-dive 섹션은 그 다음 단계로, **"왜 이렇게 동작하는가"를 내부 원리 수준에서** 설명합니다.

각 문서는 다음을 함께 다룹니다.

- 개념과 동작 원리 (다이어그램, 필요하면 계산식)
- 이 프로젝트의 실제 코드(`src/vllm_lab/`, `scripts/`, `configs/`, `deploy/`)와의 연결
- 관련 실습(`labs/`)에서 관찰한 결과의 해석

> 먼저 해당 실습을 한 번 돌려본 뒤 이 문서를 읽으면 가장 효과가 좋습니다.
> 개념만 빠르게 보고 싶다면 `appendix/`를 먼저 읽고 여기로 넘어오세요.

## 다루는 범위

이번 deep-dive는 두 묶음으로 구성됩니다.

- **1~7: 추론 최적화(inference optimization)** — "같은 GPU로 어떻게 더 빠르게, 더 많이 처리하는가".
- **8~11: 모델 효율화와 도구 선택** — 양자화, LoRA·QLoRA, sampling·guided decoding, 프레임워크 비교.

## 읽는 순서

1~7은 "토큰 하나가 만들어지는 과정 → 메모리 → 배치 → 캐싱 → 가속 → 분산 → 엔진 전체"로 이어지고,
8~11은 모델을 가볍게 만들고(양자화·LoRA) 출력을 다루며(sampling) 도구를 고르는(프레임워크) 주제입니다.

| 순서 | 문서 | 한 줄 요약 | 먼저 보면 좋은 실습 |
|---:|---|---|---|
| 1 | [추론 성능 지표](01_inference_metrics.md) | TTFT·TPOT·throughput이 무엇이고 어떻게 측정되나 | [실습 5](../labs/05_local_benchmark.md) |
| 2 | [KV cache와 PagedAttention](02_kv_cache_and_paged_attention.md) | KV cache 메모리 계산, GQA/MQA, 페이지 단위 메모리 관리 | [실습 6](../labs/06_prefix_caching.md) |
| 3 | [배치와 스케줄링](03_batching_and_scheduling.md) | 연속 배치·chunked prefill·스케줄러 토큰 예산과 튜닝 | [실습 5](../labs/05_local_benchmark.md) |
| 4 | [Prefix caching 내부 동작](04_prefix_caching_internals.md) | 블록 해시로 prefix를 공유하는 원리와 효과 조건 | [실습 6](../labs/06_prefix_caching.md) |
| 5 | [Speculative decoding](05_speculative_decoding.md) | draft 모델 제안 → 타깃 검증, 언제 이득인가 | [실습 8](../labs/08_speculative_decoding.md) |
| 6 | [멀티 GPU 병렬화](06_multi_gpu_parallelism.md) | tensor/pipeline 병렬, `-tp`의 의미와 비용 | [실습 5](../labs/05_local_benchmark.md) |
| 7 | [vLLM 엔진 아키텍처](07_vllm_engine_architecture.md) | `LLM`/`LLMEngine`/서버 계층과 요청 라이프사이클 | [실습 2](../labs/02_local_first_server.md), [실습 3](../labs/03_first_python_client.md) |
| 8 | [양자화 기법](08_quantization_methods.md) | BnB·GPTQ·AWQ·GGUF 비교, 메모리·속도·품질 trade-off | [부록 6](../appendix/06_quantization.md) |
| 9 | [LoRA와 QLoRA](09_lora_and_qlora.md) | 저랭크 adapter 원리, QLoRA, 멀티 어댑터 서빙 | [실습 7](../labs/07_lora_serving.md) |
| 10 | [Sampling과 guided decoding](10_sampling_and_guided_decoding.md) | temperature·top_p·penalty, 출력 형식 강제 | [실습 4](../labs/04_sampling.md) |
| 11 | [프레임워크 비교](11_framework_comparison.md) | vLLM·SGLang·TGI·TensorRT-LLM과 선택 기준 | [실습 1](../labs/01_why_vllm.md) |

## 입문(appendix) ↔ 심화(deep-dive) 매핑

| 입문 (appendix) | 심화 (deep-dive) |
|---|---|
| [Prefill과 decode](../appendix/03_prefill_decode.md) | [추론 성능 지표](01_inference_metrics.md), [엔진 아키텍처](07_vllm_engine_architecture.md) |
| [KV cache](../appendix/04_kv_cache.md) | [KV cache와 PagedAttention](02_kv_cache_and_paged_attention.md) |
| [Batching](../appendix/05_batching.md) | [배치와 스케줄링](03_batching_and_scheduling.md) |
| — (prefix caching은 실습에만 있음) | [Prefix caching 내부 동작](04_prefix_caching_internals.md) |
| [Quantization](../appendix/06_quantization.md) | [양자화 기법](08_quantization_methods.md) |
| [LoRA와 QLoRA](../appendix/07_lora_qlora.md) | [LoRA와 QLoRA](09_lora_and_qlora.md) |

## 관련 문서

- [전체 문서 목차](../README.md)
- [실습 챕터](../labs/) · [부록(입문 개념)](../appendix/)
