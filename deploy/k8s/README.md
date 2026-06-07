# Kubernetes kind smoke test

이 예제는 선택 경로입니다. Kubernetes 기본 지식이 있고 local kind smoke test만 확인하려는 사용자를 대상으로 합니다.

production 배포 가이드가 아닙니다.

## 시작

Apple Silicon + Colima 환경에서는 Docker VM memory를 8GiB 정도로 둡니다.

```bash
colima stop
colima start --cpu 4 --memory 8
```

Docker 실습 9 서버가 아직 실행 중이면 8000 port가 겹치므로 먼저 종료합니다.

```bash
docker compose --env-file .env -f deploy/docker/docker-compose.yml down
```

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
kubectl get pods -n vllm-lab
kubectl port-forward -n vllm-lab svc/vllm-server 8000:8000
```

다른 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

## Hugging Face Token

실제 secret은 commit하지 않습니다. token이 필요하면 example을 local 임시 파일로 복사한 뒤 직접 수정해서 적용합니다.

```bash
cp deploy/k8s/base/secret.example.yaml /tmp/hf-token-secret.yaml
kubectl apply -f /tmp/hf-token-secret.yaml
```

적용 전에 `/tmp/hf-token-secret.yaml`의 값을 수정하세요.
