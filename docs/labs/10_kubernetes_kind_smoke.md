# 실습 10: Kubernetes kind smoke test

[전체 목차](../README.md) | 이전: [실습 9](09_docker_smoke.md)

## 이번 챕터 목표

kind에서 vLLM server를 한 번 실행하고, `port-forward` 후 같은 Python client로 호출합니다.

이 챕터는 Kubernetes 기본 지식을 알고 있는 사용자를 위한 선택 smoke test입니다.

## 예상 시간

15분

## 시작 전 확인

`kind`와 `kubectl`을 사용할 수 있어야 합니다.

Apple Silicon + Colima 환경이라면 Docker VM memory를 8GiB 정도로 둡니다.

```bash
colima stop
colima start --cpu 4 --memory 8
```

Docker 실습 9 서버가 아직 켜져 있으면 port-forward와 충돌할 수 있으므로 먼저 끕니다.

```bash
docker compose --env-file .env -f deploy/docker/docker-compose.yml down
```

`.env`에는 kind smoke test용 작은 model과 CPU KV cache 값을 둡니다.

```env
MODEL_DEFAULT=Qwen/Qwen2.5-0.5B-Instruct
DEFAULT_DTYPE=float32
DEFAULT_MAX_MODEL_LEN=512
K8S_CPU_KVCACHE_SPACE=1
K8S_MAX_NUM_SEQS=1
K8S_MAX_NUM_BATCHED_TOKENS=256
```

## 실행

cluster를 만듭니다.

```bash
kind create cluster --config deploy/k8s/kind/kind-cluster.yaml
```

resource를 적용합니다.

```bash
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
kubectl get pods -n vllm-lab
```

service를 local port로 연결합니다.

```bash
kubectl port-forward -n vllm-lab svc/vllm-server 8000:8000
```

다른 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

선택적으로 benchmark도 실행할 수 있습니다.

```bash
uv run python scripts/run_benchmark.py
```

## 성공 확인

같은 Python client가 kind 위의 vLLM server에 연결되면 성공입니다.

이번 Apple Silicon + Colima kind smoke test에서는 평균 `1.600385s`, `9.997597 tok/s`, 완료 요청 `3`개를 확인했습니다. Docker smoke test보다 약간 느릴 수 있으며, kind와 `port-forward` 경로가 추가되기 때문에 자연스러운 차이입니다.

## 주의

이 예제는 production deployment가 아닙니다.

Apple Silicon kind overlay는 `vllm/vllm-openai-cpu:latest-arm64` image를 사용합니다. GPU image에서 `Failed to infer device type`이 나오면 CPU image overlay가 적용됐는지 확인하세요.

## 다음 단계

필요한 개념은 [부록](../README.md#3-부록)에서 골라 읽으세요.
