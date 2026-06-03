# Kubernetes kind smoke test

이 예제는 선택 경로입니다. Kubernetes 기본 지식이 있고 local kind smoke test만 확인하려는 사용자를 대상으로 합니다.

production 배포 가이드가 아닙니다.

## 시작

```bash
kind create cluster --config deploy/k8s/kind/kind-cluster.yaml
kubectl apply -f deploy/k8s/base/namespace.yaml
kubectl create configmap vllm-lab-env -n vllm-lab --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -k deploy/k8s/overlays/kind-smoke
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
