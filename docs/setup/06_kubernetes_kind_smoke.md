# Kubernetes kind smoke test 준비

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

이미 Kubernetes 기본 지식이 있고, kind에서 vLLM server smoke test를 해보고 싶을 때 읽습니다.

이 문서는 Kubernetes 기초를 설명하지 않습니다.

## 도구 확인

```bash
kind version
kubectl version --client
```

도구가 없다면 설치합니다.

```bash
brew install kind kubectl
```

Apple Silicon + Colima 환경에서는 Docker VM memory를 8GiB 정도로 둡니다.

```bash
colima stop
colima start --cpu 4 --memory 8
```

Docker 실습 9 서버가 아직 실행 중이면 8000 port가 겹치므로 먼저 종료합니다.

```bash
docker compose --env-file .env -f deploy/docker/docker-compose.yml down
```

## 실행

```bash
kind create cluster --config deploy/k8s/kind/kind-cluster.yaml
```

namespace와 `.env` 기반 config를 적용합니다.

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
```

smoke test resource를 적용합니다.

```bash
kubectl kustomize --load-restrictor=LoadRestrictionsNone deploy/k8s/overlays/kind-smoke | kubectl apply -f -
kubectl get pods -n vllm-lab
kubectl port-forward -n vllm-lab svc/vllm-server 8000:8000
```

다른 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

## 주의

이 예제는 production Kubernetes 배포가 아닙니다.

## 다음 문서

[실습 10: Kubernetes kind smoke test](../labs/10_kubernetes_kind_smoke.md)
