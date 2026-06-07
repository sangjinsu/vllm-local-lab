# vLLM Local Lab

vLLM을 로컬에서 실행하고 Python으로 호출해 보며 LLM serving의 기본 흐름을 단계적으로 익히는 local-first 학습 프로젝트입니다.

이 프로젝트는 production LLM platform 가이드가 아닙니다. 먼저 작은 모델을 로컬에서 실행하고, 같은 OpenAI-compatible Python client로 호출하고, 설정을 바꿔 보며 결과를 비교하는 데 집중합니다.

## 핵심 원칙

- 기본 학습 경로는 local `vllm serve`입니다.
- Docker와 Kubernetes kind는 선택 smoke test입니다.
- RunPod은 사용하지 않습니다.
- 공통 설정은 `.env`로 관리합니다.
- 실제 token이나 secret은 commit하지 않습니다.

## 누구를 위한 프로젝트인가요?

기본적인 Python은 알고 있지만 vLLM이나 LLM serving은 처음인 사용자를 대상으로 합니다.

이 프로젝트를 따라가면 다음을 할 수 있습니다.

- `.env`로 model, server, sampling, benchmark 설정 관리
- local vLLM server 실행
- Python client로 OpenAI-compatible API 호출
- `temperature`, `top_p`, `max_tokens` 변경
- latency와 throughput benchmark 생성
- prefix caching, LoRA serving, speculative decoding을 실습 수준에서 확인
- Docker와 Kubernetes kind에서 같은 Python client로 smoke test 실행

## 빠른 시작

먼저 Python dependency와 `.env`를 준비합니다.

```bash
uv sync --extra dev
cp .env.example .env
```

리소스가 제한된 환경에서 처음 실행한다면 `.env`에서 작은 model profile을 사용하세요.

```env
MODEL_PROFILE=tiny
```

server 실행 명령을 확인합니다.

```bash
uv run python scripts/local_serve_help.py
```

출력된 `vllm serve ...` 명령을 첫 번째 터미널에서 실행합니다.

두 번째 터미널에서 server 연결을 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

Apple Silicon macOS에서 문제가 생기면 [Apple Silicon 환경](docs/setup/04_apple_silicon.md)과 [문제 해결](docs/setup/07_troubleshooting.md)을 먼저 확인하세요.

## 학습 경로

전체 문서 목차는 [docs/README.md](docs/README.md)에서 시작합니다.

권장 순서는 다음과 같습니다.

1. [환경 선택](docs/setup/00_choose_your_environment.md)
2. [공통 `.env` 설정](docs/setup/01_common_env.md)
3. [실습 1: vLLM을 왜 쓰나요?](docs/labs/01_why_vllm.md)
4. [실습 2: 로컬 vLLM 서버 실행](docs/labs/02_local_first_server.md)
5. [실습 3: 첫 Python client 호출](docs/labs/03_first_python_client.md)
6. [실습 4: Sampling 설정 바꾸기](docs/labs/04_sampling.md)
7. [실습 5: 로컬 benchmark](docs/labs/05_local_benchmark.md)
8. [실습 6: Prefix caching](docs/labs/06_prefix_caching.md)
9. [실습 7: LoRA serving](docs/labs/07_lora_serving.md)
10. [실습 8: Speculative decoding](docs/labs/08_speculative_decoding.md)
11. [실습 9: Docker smoke test](docs/labs/09_docker_smoke.md)
12. [실습 10: Kubernetes kind smoke test](docs/labs/10_kubernetes_kind_smoke.md)

## Model Profile

`MODEL_PROFILE` 값으로 사용할 model을 고릅니다. Python 코드가 profile을 해석하므로 `.env`에서 `DEFAULT_MODEL=${MODEL_DEFAULT}` 같은 shell expansion에 의존하지 않습니다.

| Profile | Model | 용도 |
|---|---|---|
| `tiny` | `Qwen/Qwen2.5-0.5B-Instruct` | 제한된 리소스에서 첫 성공 확인 |
| `default` | `Qwen/Qwen3-0.6B` | 기본 로컬 학습 모델 |
| `small-chat` | `Qwen/Qwen2.5-1.5B-Instruct` | 조금 더 나은 chat 품질 |
| `balanced` | `Qwen/Qwen2.5-3B-Instruct` | 리소스가 충분한 로컬 GPU 실습 |
| `advanced` | `meta-llama/Llama-3.2-3B-Instruct` | 선택 고급 모델, Hugging Face 접근 권한이 필요할 수 있음 |

## Benchmark

단일 benchmark:

```bash
uv run python scripts/run_benchmark.py
```

`.env`의 matrix 값으로 여러 조합 실행:

```bash
uv run python scripts/run_benchmark_matrix.py
```

결과는 다음 위치에 생성됩니다.

```text
results/benchmarks/latest.csv
results/benchmarks/latest.md
```

실제 Apple Silicon 환경에서 진행한 테스트 과정과 benchmark 해석은 [2026-06-07 Apple Silicon smoke test 기록](docs/test-runs/2026-06-07_apple_silicon_smoke.md)에 정리되어 있습니다.

## 선택 Smoke Test

Docker와 Kubernetes kind는 기본 학습 경로가 아닙니다. local server와 Python client 호출을 먼저 성공한 뒤 진행하세요.

| 경로 | 문서 | 목적 |
|---|---|---|
| Docker | [Docker smoke test](docs/labs/09_docker_smoke.md) | container에서 같은 Python client 호출 확인 |
| Kubernetes kind | [Kubernetes kind smoke test](docs/labs/10_kubernetes_kind_smoke.md) | kind Pod와 Service를 port-forward 후 호출 확인 |

Kubernetes kind 문서는 Kubernetes 기본 지식이 있는 사용자를 대상으로 합니다. Kubernetes 기초나 production 배포를 설명하지 않습니다.

## 보안

`.env`, 실제 Hugging Face token, secret 값을 commit하지 마세요.

- `.env.example`은 template입니다.
- `deploy/k8s/base/secret.example.yaml`은 예시 Secret입니다.
- `HF_TOKEN`은 local `.env` 또는 사용자가 직접 만든 Kubernetes Secret에만 둡니다.
- `.env` 전체를 Kubernetes ConfigMap으로 넣지 마세요.

## 문서 바로가기

- [문서 목차](docs/README.md)
- [문제 해결](docs/setup/07_troubleshooting.md)
- [Benchmark report template](docs/labs/05_benchmark_report_template.md)
- [Mermaid 요약](docs/appendix/08_mermaid_summary.md)
