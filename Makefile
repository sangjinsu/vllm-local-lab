PYTHON ?= uv run python
PYTEST ?= uv run --extra dev pytest

setup:
	uv sync --extra dev

health:
	$(PYTHON) scripts/healthcheck.py

chat:
	$(PYTHON) scripts/call_chat.py

sampling:
	$(PYTHON) scripts/run_sampling_test.py

benchmark:
	$(PYTHON) scripts/run_benchmark.py

benchmark-matrix:
	$(PYTHON) scripts/run_benchmark_matrix.py

docker-up:
	docker compose -f deploy/docker/docker-compose.yml up

docker-down:
	docker compose -f deploy/docker/docker-compose.yml down

k8s-create:
	kind create cluster --config deploy/k8s/kind/kind-cluster.yaml

k8s-apply:
	kubectl apply -k deploy/k8s/overlays/kind-smoke

k8s-forward:
	kubectl port-forward -n vllm-lab svc/vllm-server 8000:8000

test:
	$(PYTEST) -q
