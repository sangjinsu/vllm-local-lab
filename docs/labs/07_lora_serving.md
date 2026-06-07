# 실습 7: LoRA serving

[전체 목차](../README.md) | 이전: [실습 6](06_prefix_caching.md) | 다음: [실습 8](08_speculative_decoding.md)

## 이번 챕터 목표

이미 가지고 있는 LoRA adapter를 vLLM server에 연결할 때 필요한 설정과 파일 구조를 확인합니다.

이 챕터는 LoRA training을 다루지 않습니다.

## 예상 시간

10분

## 시작 전 확인

이 실습에는 두 단계가 있습니다.

1. 예시 adapter 디렉터리로 `.env` 설정과 파일 구조를 확인합니다.
2. 실제 학습된 adapter가 있을 때 vLLM server에 연결합니다.

예시 adapter는 경로와 파일 이름을 배우기 위한 용도입니다. 실제 LoRA 효과를 보려면 학습된 adapter 파일이 필요합니다.

## adapter 디렉터리 구조

`LORA_MODULE_PATH`가 가리키는 디렉터리에는 최소한 다음 파일이 있어야 합니다.

```text
adapter_config.json
adapter_model.safetensors
```

예시용 placeholder 파일은 구조 확인에는 충분하지만, 실제 serving 성공을 보장하지 않습니다.

## 실행

`.env`를 설정합니다.

```env
ENABLE_LORA=true
LORA_MODULE_NAME=my-adapter
LORA_MODULE_PATH=/Users/<your-name>/Models/my-lora-adapter
```

설정을 확인합니다.

```bash
uv run python scripts/run_lora_test.py
```

## 성공 확인

다음 내용이 보이면 설정과 기본 파일 구조 확인은 성공입니다.

```text
LORA_MODULE_NAME=my-adapter
LORA_MODULE_PATH=...
adapter_config.json: ok
adapter_model.safetensors: ok
```

`adapter_model.safetensors`가 매우 작다는 경고가 나오면 placeholder 파일일 수 있습니다. 이 경우에는 “경로와 구조 확인”까지만 성공한 상태입니다.

## 실제 adapter로 server 시작

실제 학습된 adapter가 준비되어 있다면 server 명령을 다시 출력합니다.

```bash
uv run python scripts/local_serve_help.py
```

`ENABLE_LORA=true`, `LORA_MODULE_NAME`, `LORA_MODULE_PATH`가 모두 설정되어 있으면 다음 옵션이 함께 출력됩니다.

```bash
--enable-lora
--lora-modules my-adapter=/Users/<your-name>/Models/my-lora-adapter
```

출력된 `vllm serve ...` 명령을 server 터미널에서 실행합니다. 서버가 떠 있는지만 먼저 확인합니다.

```bash
uv run python scripts/healthcheck.py
```

LoRA adapter를 호출할 때는 OpenAI-compatible request의 `model` 값에 `LORA_MODULE_NAME`을 사용합니다. 이 프로젝트의 기본 `scripts/call_chat.py`는 base model 연결 확인용이므로, 실제 adapter 응답을 확인할 때는 요청의 `model` 값을 adapter 이름으로 바꾸어 호출해야 합니다.

```bash
uv run python - <<'PY'
from vllm_lab.client import create_client
from vllm_lab.config import settings

client = create_client()
response = client.chat.completions.create(
    model=settings.lora_module_name,
    messages=[
        {"role": "user", "content": "한 문장으로 이 adapter가 연결되었는지 확인해 주세요."}
    ],
    temperature=settings.default_temperature,
    top_p=settings.default_top_p,
    max_tokens=settings.default_max_tokens,
)
print(response.choices[0].message.content)
PY
```

## 자주 막히는 지점

- `LORA_MODULE_PATH`가 비어 있으면 script가 실패합니다.
- `LORA_MODULE_PATH=/path/to/local/adapter`처럼 문서 placeholder를 그대로 쓰면 실패합니다.
- `adapter_config.json` 또는 `adapter_model.safetensors`가 없으면 실제 LoRA serving을 시작할 수 없습니다.
- placeholder `adapter_model.safetensors`는 실제 학습된 weight가 아니므로 server 시작 또는 응답 품질 검증에는 사용할 수 없습니다.

## 다음 챕터

[실습 8: Speculative decoding](08_speculative_decoding.md)
