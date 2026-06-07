# 문제 해결

[문서 목차로 돌아가기](../README.md)

## client가 연결되지 않을 때

먼저 server 명령을 확인합니다.

```bash
uv run python scripts/local_serve_help.py
```

출력된 `vllm serve ...` 명령을 실행한 뒤 다시 확인합니다.

```bash
uv run python scripts/healthcheck.py
```

## `zsh: command not found: vllm`

`vllm` CLI가 현재 shell에서 보이지 않는 상태입니다.

vLLM source build 환경을 사용 중이라면 venv를 활성화했는지 확인합니다.

```bash
cd ~/Projects/vendor/vllm
source .venv/bin/activate
which vllm
vllm --help
```

이 repo의 기본 `uv sync --extra dev`는 Python client 학습용 dependency만 설치합니다. vLLM server 실행 환경은 별도로 준비할 수 있습니다.

## `nvidia-cudnn-frontend` wheel 오류

Apple Silicon macOS에서 다음과 비슷한 오류가 날 수 있습니다.

```text
nvidia-cudnn-frontend ... can't be installed because it doesn't have a source distribution or wheel for the current platform
```

이 경우 `uv sync --extra serve`를 계속 반복하지 마세요. macOS arm64에서 CUDA/NVIDIA 계열 wheel이 없어 생기는 resolver 실패입니다.

대신 [Apple Silicon 환경](04_apple_silicon.md)의 vLLM source build 경로를 사용하세요.

## 모델이 메모리에 올라가지 않을 때

작은 profile을 사용합니다.

```env
MODEL_PROFILE=tiny
DEFAULT_MAX_MODEL_LEN=2048
```

`.env`를 바꾼 뒤에는 vLLM server를 다시 시작하세요.

CPU backend에서 다음과 비슷한 오류가 날 수도 있습니다.

```text
Available memory ... is less than desired CPU memory utilization
```

CPU backend에서는 이름과 달리 `--gpu-memory-utilization`이 CPU memory 예약 비율에도 영향을 줍니다. Mac mini처럼 여유 메모리가 적은 환경에서는 낮게 시작하세요.

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

## `No available shared memory broadcast block found`

server는 떠 있지만 generation worker가 compilation 또는 무거운 작업에서 오래 걸리는 상태일 수 있습니다.

Apple Silicon CPU backend에서는 server를 `Ctrl-C`로 끊고 다음처럼 compile 부담을 줄여 다시 시작하세요.

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

그래도 느리면 `--max-model-len 256`, `--gpu-memory-utilization 0.15`, `--max-num-batched-tokens 256`까지 낮춰 마지막으로 확인합니다.

## speculative config가 인자로 인식되지 않을 때

다음처럼 JSON을 다음 줄에 따로 쓰면 shell은 `--speculative-config`의 값을 받지 못합니다.

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
  --speculative-config
  '{"method":"ngram","num_speculative_tokens":4}'
```

한 줄 인자로 넘기세요.

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
  --speculative-config '{"method":"ngram","num_speculative_tokens":1,"prompt_lookup_min":2,"prompt_lookup_max":5}'
```

Apple Silicon CPU 환경에서는 작은 값부터 확인합니다.

```env
DEFAULT_TEMPERATURE=0
DEFAULT_TOP_P=1.0
SPECULATIVE_CONFIG_JSON={"method":"ngram","num_speculative_tokens":1,"prompt_lookup_min":2,"prompt_lookup_max":5}
```

## `maximum context length` 또는 `400 Bad Request`

다음과 비슷한 오류는 입력 prompt와 출력 token이 server의 context 길이를 넘었다는 뜻입니다.

```text
maximum context length is 256 tokens
you requested 256 output tokens
```

`max-model-len`은 입력 prompt와 출력 token을 합친 전체 한도입니다. `--max-model-len 256`으로 server를 띄우고 `DEFAULT_MAX_TOKENS=256`을 요청하면 입력 prompt가 들어갈 공간이 없습니다.

`.env`에서 출력 token을 낮추세요.

```env
DEFAULT_MAX_TOKENS=32
```

그 다음 다시 호출합니다.

```bash
uv run python scripts/call_chat.py
```

## 답변 내용이 틀릴 때

local server 호출이 성공해도 작은 모델이 틀린 답을 할 수 있습니다. 예를 들어 vLLM을 잘못 풀이하는 답변이 나올 수 있습니다.

setup 단계에서는 먼저 `Python client → localhost:8000/v1 → vLLM server` 경로가 열렸는지 확인하는 것이 목표입니다. 답변 품질은 model 크기, prompt, sampling, `DEFAULT_MAX_TOKENS`를 조정하면서 별도로 봅니다.

## Docker에서 `Failed to infer device type`이 나올 때

Apple Silicon + Colima처럼 GPU가 없는 Docker 환경에서 GPU image를 실행하면 device type 추론에 실패할 수 있습니다.

CPU image를 사용하세요.

```env
DOCKER_IMAGE=vllm/vllm-openai-cpu:latest-arm64
DEFAULT_DTYPE=float32
DEFAULT_MAX_MODEL_LEN=512
DOCKER_CPU_KVCACHE_SPACE=1
DOCKER_MAX_NUM_SEQS=1
DOCKER_MAX_NUM_BATCHED_TOKENS=256
```

Colima memory가 부족하면 모델 로딩 또는 KV cache allocation에서 실패할 수 있습니다.

```bash
colima stop
colima start --cpu 4 --memory 8
```

## kind에서 memory 또는 port 문제가 날 때

kind는 Colima 위에서 동작하므로 Colima memory가 너무 작으면 Pod가 시작하지 못할 수 있습니다.

```bash
kubectl get pods -n vllm-lab
kubectl logs -n vllm-lab deploy/vllm-server --tail=100
```

Docker 실습 9 container가 아직 8000 port를 사용하고 있으면 `port-forward`와 충돌할 수 있습니다.

```bash
docker compose --env-file .env -f deploy/docker/docker-compose.yml down
kubectl port-forward -n vllm-lab svc/vllm-server 8000:8000
```

## LoRA adapter 경로가 실패할 때

`LORA_MODULE_PATH`에는 실제 디렉터리 경로를 넣어야 합니다.

다음 값은 문서용 placeholder라서 그대로 쓰면 동작하지 않습니다.

```env
LORA_MODULE_PATH=/path/to/local/adapter
```

Mac에서 예시 adapter를 만든 경우처럼 실제 경로를 사용하세요.

```env
LORA_MODULE_PATH=/Users/<your-name>/Models/my-lora-adapter
```

다음 명령으로 구조를 먼저 확인합니다.

```bash
uv run python scripts/run_lora_test.py
```

## LoRA adapter 파일이 없을 때

`run_lora_test.py`가 다음 파일을 확인합니다.

```text
adapter_config.json
adapter_model.safetensors
```

둘 중 하나라도 `missing`이면 실제 LoRA serving을 시작할 수 없습니다. adapter를 다시 내려받거나, 학습 결과물이 저장된 디렉터리를 `LORA_MODULE_PATH`로 지정하세요.

## placeholder adapter를 실제 serving에 쓰려 할 때

예시 학습용으로 만든 `adapter_model.safetensors`가 매우 작다면 실제 LoRA weight가 아닐 가능성이 큽니다.

이 파일은 `.env` 설정, directory 구조, script 검증 흐름을 배우기 위한 placeholder입니다. 실제 LoRA 효과를 확인하려면 학습된 adapter의 `adapter_config.json`과 `adapter_model.safetensors`를 사용해야 합니다.

## Hugging Face 접근이 실패할 때

일부 선택 모델은 Hugging Face 접근 권한이 필요할 수 있습니다.

local `.env`에만 `HF_TOKEN`을 설정하세요. 실제 token은 commit하지 않습니다.

## benchmark가 너무 오래 걸릴 때

작은 값부터 시작합니다.

```env
BENCHMARK_NUM_PROMPTS=5
BENCHMARK_REQUEST_RATE=1
BENCHMARK_MAX_TOKENS_LIST=64
```

## 다음 문서

문제가 해결되면 [문서 목차](../README.md)에서 진행하던 챕터로 돌아가세요.
