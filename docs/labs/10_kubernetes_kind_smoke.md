# 실습 10: Kubernetes kind smoke test

[전체 목차](../README.md) | 이전: [실습 9](09_docker_smoke.md)

## 이번 챕터 목표

kind에서 vLLM server를 한 번 실행하고, `port-forward` 후 같은 Python client로 호출합니다.

이 챕터는 Kubernetes 기본 지식을 알고 있는 사용자를 위한 선택 smoke test입니다.

## 예상 시간

15분

## 시작 전 확인

`kind`와 `kubectl`을 사용할 수 있어야 합니다.

## 실행

cluster를 만듭니다.

```bash
kind create cluster --config deploy/k8s/kind/kind-cluster.yaml
```

resource를 적용합니다.

```bash
kubectl apply -f deploy/k8s/base/namespace.yaml
kubectl create configmap vllm-lab-env -n vllm-lab --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -k deploy/k8s/overlays/kind-smoke
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

## 성공 확인

같은 Python client가 kind 위의 vLLM server에 연결되면 성공입니다.

## 주의

이 예제는 production deployment가 아닙니다.

## 다음 단계

필요한 개념은 [부록](../README.md#3-부록)에서 골라 읽으세요.
