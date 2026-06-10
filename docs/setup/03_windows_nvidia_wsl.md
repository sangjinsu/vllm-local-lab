# Windows NVIDIA WSL 환경

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

Windows에서 WSL을 사용하고 NVIDIA GPU를 연결해 실습하려는 경우 읽습니다.

## 준비

WSL 안에서 실행합니다.

```bash
uv sync --extra dev
cp .env.example .env
```

처음에는 작은 모델을 권장합니다.

```env
MODEL_PROFILE=tiny
```

## 8GB GPU 권장 `.env`

`uv sync --extra serve`로 설치한 pip wheel vLLM을 WSL에서 띄울 때, 8GB GPU(RTX 5060 등)에서는 다음 설정을 권장합니다.

```env
DEFAULT_GPU_MEMORY_UTILIZATION=0.80
ENFORCE_EAGER=true
DISABLE_FLASHINFER_SAMPLER=true
```

이 값을 설정하면 `local_serve_help.py`가 serve 명령에 해당 옵션을 자동으로 붙여 줍니다. 이유는 아래 "자주 막히는 지점"을 참고하세요.

## 실행

```bash
uv run python scripts/local_serve_help.py
```

출력된 `vllm serve ...` 명령을 실행한 뒤, 다른 터미널에서 확인합니다.

```bash
uv run python scripts/healthcheck.py
uv run python scripts/call_chat.py
```

## 자주 막히는 지점

client가 연결되지 않으면 `VLLM_PORT`와 server가 실제로 listening 중인 port가 같은지 확인하세요.

### server가 모델 로딩 직후 조용히 멈출 때 (FlashInfer / nvcc)

증상: server 로그가 `Using FlashAttention version 2` 또는 sampler 초기화 부근에서 더 진행되지 않고, 결국 `Could not find nvcc and default cuda_home='/usr/local/cuda' doesn't exist` 오류가 납니다.

원인: pip wheel로 설치한 vLLM에는 CUDA 런타임만 있고 `nvcc`(CUDA Toolkit)가 없어, FlashInfer가 top-k/top-p sampler 커널을 JIT 컴파일하지 못합니다.

해결: `.env`에 `DISABLE_FLASHINFER_SAMPLER=true`를 설정하면 serve 명령 앞에 `VLLM_USE_FLASHINFER_SAMPLER=0`이 붙어 네이티브 sampler로 우회합니다. FlashInfer 성능이 필요하면 WSL에 CUDA Toolkit을 설치해 `nvcc`를 제공하세요.

### `Free memory ... is less than desired GPU memory utilization`

원인: Windows가 GPU를 상시 약 1GB 점유하므로, vLLM 기본값 `--gpu-memory-utilization 0.92`는 8GB GPU에서 메모리 부족으로 실패합니다.

해결: `.env`에 `DEFAULT_GPU_MEMORY_UTILIZATION=0.80`을 설정하세요.

### 기동이 너무 느릴 때

WSL에서는 `torch.compile`/cudagraph 캡처 단계가 매우 느릴 수 있습니다. smoke test에서는 `.env`에 `ENFORCE_EAGER=true`를 설정해 이 단계를 건너뛰면 기동이 빨라집니다.

## 다음 문서

[실습 1: vLLM을 왜 쓰나요?](../labs/01_why_vllm.md)
