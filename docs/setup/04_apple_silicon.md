# Apple Silicon 환경

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

Apple Silicon macOS에서 가능한 범위의 로컬 실습을 확인하려는 경우 읽습니다.

## 준비

```bash
uv sync --extra dev
cp .env.example .env
```

처음에는 작은 설정을 권장합니다.

```env
MODEL_PROFILE=tiny
DEFAULT_DTYPE=auto
DEFAULT_MAX_MODEL_LEN=2048
```

## 먼저 알아둘 점

Apple Silicon macOS에서는 `uv sync --extra serve`가 바로 성공하지 않을 수 있습니다. 예를 들어 `nvidia-cudnn-frontend`가 macOS arm64 wheel을 제공하지 않아 설치가 실패할 수 있습니다.

이 프로젝트의 lab client와 vLLM server는 같은 virtualenv에 있을 필요가 없습니다. vLLM server는 별도 환경에서 실행하고, 이 repo는 `VLLM_BASE_URL`로 HTTP 호출만 하면 됩니다.

## vLLM source build

Apple Silicon에서 vLLM server를 직접 실행하려면 별도 위치에 vLLM을 source build하는 경로를 권장합니다.

```bash
mkdir -p ~/Projects/vendor
cd ~/Projects/vendor

git clone https://github.com/vllm-project/vllm.git
cd vllm

uv venv --python 3.12
source .venv/bin/activate

uv pip install -r requirements/cpu.txt --index-strategy unsafe-best-match
uv pip install -e .
```

설치 확인:

```bash
vllm --help
```

## Mac CPU 권장 server 명령

Mac mini/Apple Silicon CPU backend에서는 먼저 작은 context와 eager mode로 시작하세요.

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype float32 \
  --max-model-len 512 \
  --gpu-memory-utilization 0.2 \
  --enforce-eager \
  --max-num-seqs 1 \
  --max-num-batched-tokens 512
```

server가 떠 있으면 이 repo로 돌아와 확인합니다.

```bash
cd /Users/sangjinsu/Projects/vllm-local-lab
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

## 일반 명령 출력 확인

Linux/NVIDIA 같은 기본 local-first 환경에서는 다음 helper를 사용할 수 있습니다.

```bash
uv run python scripts/local_serve_help.py
```

Apple Silicon CPU backend에서는 위 helper가 출력하는 일반 명령보다 `Mac CPU 권장 server 명령`을 먼저 사용하세요.

## 자주 막히는 지점

- `zsh: command not found: vllm`이 나오면 vLLM source build venv가 활성화되어 있는지 확인하세요.
- `nvidia-cudnn-frontend` wheel 오류가 나오면 이 repo에서 `uv sync --extra serve`를 계속 시도하지 말고 source build 경로를 사용하세요.
- `No available shared memory broadcast block found`가 반복되면 `--enforce-eager`, `--dtype float32`, 더 작은 `--max-model-len`을 사용하세요.
- `maximum context length` 오류가 나오면 `.env`의 `DEFAULT_MAX_TOKENS`를 `32`처럼 낮추세요.

Apple Silicon의 vLLM 지원과 성능은 설치 방식과 vLLM 버전에 따라 달라질 수 있습니다. 이 경우에도 Python client, `.env`, benchmark 구조는 그대로 학습할 수 있습니다.

Docker와 Kubernetes는 여전히 선택 smoke test이며 기본 학습 경로가 아닙니다.

## 다음 문서

[실습 1: vLLM을 왜 쓰나요?](../labs/01_why_vllm.md)
