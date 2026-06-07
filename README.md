# vLLM Local Lab

# 공사중 / 테스트 중

## 현재 이 프로젝트는 안정 버전이 아닙니다.

**실제 local setup을 검증하면서 문서와 예제를 계속 조정하는 중입니다.**

특히 Apple Silicon macOS의 vLLM 실행 경로는 설치 방식과 vLLM 버전에 따라 달라질 수 있습니다. 문제가 생기면 [Apple Silicon 환경](docs/setup/04_apple_silicon.md)과 [문제 해결](docs/setup/07_troubleshooting.md)을 먼저 확인하세요.

---

로컬에서 vLLM을 실행하고 Python으로 호출해 보며, LLM serving의 실무 감각을 단계적으로 익히는 학습 프로젝트입니다.

이 프로젝트의 기준은 다음과 같습니다.

- 기본 학습 경로는 local `vllm serve`입니다.
- Docker와 Kubernetes는 선택 smoke test입니다.
- RunPod은 사용하지 않습니다.
- 공통 설정은 `.env`로 관리합니다.
- 실제 token이나 secret은 commit하지 않습니다.

## 누구를 위한 프로젝트인가요?

기본적인 Python은 알고 있지만 vLLM이나 LLM serving은 처음인 사용자를 대상으로 합니다.

이 프로젝트는 production LLM platform 가이드가 아닙니다. 먼저 로컬에서 작은 모델을 실행하고, 같은 Python client로 호출하고, 설정을 바꿔 보며 결과를 비교하는 데 집중합니다.

## 빠른 시작

```bash
uv sync --extra dev
cp .env.example .env
uv run python scripts/local_serve_help.py
```

출력된 `vllm serve ...` 명령을 첫 번째 터미널에서 실행합니다.

두 번째 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

리소스가 제한된 환경에서 처음 실행한다면 `.env`에서 다음 값을 권장합니다.

```env
MODEL_PROFILE=tiny
```

## 학습 목차

전체 문서 목차는 [docs/README.md](docs/README.md)에서 시작하세요.

추천 순서:

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

| Profile | Model | 용도 |
|---|---|---|
| `tiny` | `Qwen/Qwen2.5-0.5B-Instruct` | 제한된 리소스에서 첫 성공 확인 |
| `default` | `Qwen/Qwen3-0.6B` | 기본 로컬 학습 모델 |
| `small-chat` | `Qwen/Qwen2.5-1.5B-Instruct` | 조금 더 나은 chat 품질 |
| `balanced` | `Qwen/Qwen2.5-3B-Instruct` | 리소스가 충분한 로컬 GPU 실습 |
| `advanced` | `meta-llama/Llama-3.2-3B-Instruct` | 선택 고급 모델, Hugging Face 접근 권한이 필요할 수 있음 |

모델은 Python 코드가 `MODEL_PROFILE`을 기준으로 해석합니다. `.env`에서 `DEFAULT_MODEL=${MODEL_DEFAULT}` 같은 shell expansion에 의존하지 않습니다.

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

## 선택 Smoke Test

Docker:

```bash
docker compose --env-file .env -f deploy/docker/docker-compose.yml up
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
docker compose --env-file .env -f deploy/docker/docker-compose.yml down
```

Kubernetes kind는 Kubernetes 기본 지식이 있는 사용자만 진행하세요.

```bash
kind create cluster --config deploy/k8s/kind/kind-cluster.yaml
kubectl apply -f deploy/k8s/base/namespace.yaml
kubectl create configmap vllm-lab-env -n vllm-lab \
  --from-literal=MODEL_DEFAULT=Qwen/Qwen2.5-0.5B-Instruct \
  --from-literal=DEFAULT_DTYPE=float32 \
  --from-literal=DEFAULT_MAX_MODEL_LEN=512 \
  --from-literal=K8S_CPU_KVCACHE_SPACE=1 \
  --from-literal=K8S_CPU_OMP_THREADS_BIND=auto \
  --from-literal=K8S_MAX_NUM_SEQS=1 \
  --from-literal=K8S_MAX_NUM_BATCHED_TOKENS=256 \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl kustomize --load-restrictor=LoadRestrictionsNone deploy/k8s/overlays/kind-smoke | kubectl apply -f -
kubectl port-forward -n vllm-lab svc/vllm-server 8000:8000
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

Kubernetes 예제는 production 배포 가이드가 아닙니다.

## 보안

`.env`, 실제 Hugging Face token, secret 값을 commit하지 마세요. `.env.example`과 `deploy/k8s/base/secret.example.yaml`은 템플릿으로만 사용합니다.
