# Kubernetes kind smoke test 준비

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

이미 Kubernetes 기본 지식이 있고, kind에서 vLLM server smoke test를 해보고 싶을 때 읽습니다.

이 문서는 Kubernetes 기초를 설명하지 않습니다.

## 실행

```bash
kind create cluster --config deploy/k8s/kind/kind-cluster.yaml
```

namespace와 `.env` 기반 config를 적용합니다.

```bash
kubectl apply -f deploy/k8s/base/namespace.yaml
kubectl create configmap vllm-lab-env -n vllm-lab --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -
```

smoke test resource를 적용합니다.

```bash
kubectl apply -k deploy/k8s/overlays/kind-smoke
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
