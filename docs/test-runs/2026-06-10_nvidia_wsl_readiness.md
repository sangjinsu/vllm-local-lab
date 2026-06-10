# 2026-06-10 NVIDIA WSL Readiness Review

This was a readiness and smoke-path review for the local-first vLLM lab on a Windows NVIDIA machine.

## Target

- Intended runtime path: WSL2 Ubuntu
- Intended model profile: `tiny`
- Intended scope: local path only
- Docker and Kubernetes kind were not executed in this review

## Environment Observed

| Check | Result |
|---|---|
| Windows NVIDIA GPU | Detected |
| GPU | NVIDIA GeForce RTX 5060 |
| Driver | 591.74 |
| CUDA reported by driver | 13.1 |
| VRAM | 8151 MiB total; initially about 7700 MiB in use, later about 509 MiB in use |
| WSL status | WSL default version 2 is configured |
| WSL distributions | No Linux distribution is installed |
| Windows Python | Not installed globally; `uv` downloaded managed Python 3.11.15 |
| Windows `uv` | Installed to `C:\Users\NHN\.local\bin` |

## Repo Changes Made

Created local `.env` from the project defaults with conservative NVIDIA smoke-test values:

- `MODEL_PROFILE=tiny`
- `DEFAULT_MAX_MODEL_LEN=2048`
- `DEFAULT_MAX_TOKENS=64`
- `BENCHMARK_NUM_PROMPTS=5`
- `BENCHMARK_REQUEST_RATE=1`
- `BENCHMARK_MAX_CONCURRENCY=2`
- Benchmark matrix reduced to a single tiny/short run

The `.env` file is ignored by Git and contains no secrets.

## Static Checks

| Check | Result |
|---|---|
| RunPod references outside policy text | None found |
| k3d/minikube/Colab references | None found |
| Obvious Hugging Face token patterns | None found |
| User-facing script messages | `rg` shows readable Korean strings |
| Common config loading | Scripts route through `vllm_lab.config.settings` |
| Unit tests | `12 passed` with `uv run --python 3.11 --extra dev pytest -q` |

## Runtime Checks

The helper command ran successfully on Windows after installing `uv`:

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype auto \
  --max-model-len 2048
```

An existing server was briefly detected on `localhost:8000`, but it was not the server requested by this `.env`.

| Check | Result |
|---|---|
| `/health` | Initially passed against an already-running server |
| `/v1/models` | Reported `Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4`, not the configured tiny model |
| `scripts/call_chat.py` | Failed with model-not-found while `.env` requested `Qwen/Qwen2.5-0.5B-Instruct` |
| `scripts/call_completion.py` | Failed with model-not-found for the same reason |
| Later `/health` retry | Failed because the existing server was no longer listening |

Runtime checks for starting the intended NVIDIA vLLM server could not be completed because the target WSL2 Ubuntu runtime is not installed.

Blocked commands:

```bash
uv run python scripts/run_sampling_test.py
uv run python scripts/run_benchmark.py
```

## Required Next Steps

1. Install a WSL2 Ubuntu distribution.
2. In Ubuntu, confirm GPU access with `nvidia-smi`.
3. Install `uv` in Ubuntu.
4. From the repo path inside WSL, run:

```bash
uv sync --extra dev --extra serve
uv run pytest -q
uv run python scripts/local_serve_help.py
```

5. Start the printed `vllm serve ...` command in one terminal.
6. In another terminal, run:

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
uv run python scripts/run_sampling_test.py
uv run python scripts/run_benchmark.py
```

## Result

This was not a successful NVIDIA vLLM runtime smoke test. Windows-side `uv`, managed Python, `.env`, static checks, and unit tests are now in place, but the machine is still missing the WSL2 Ubuntu runtime required to start the intended local NVIDIA vLLM server path.
