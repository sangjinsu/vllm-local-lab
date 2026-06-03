# 실습 7: LoRA serving

[전체 목차](../README.md) | 이전: [실습 6](06_prefix_caching.md) | 다음: [실습 8](08_speculative_decoding.md)

## 이번 챕터 목표

이미 가지고 있는 LoRA adapter를 serving에 연결할 때 필요한 설정을 확인합니다.

이 챕터는 LoRA training을 다루지 않습니다.

## 예상 시간

10분

## 시작 전 확인

사용할 LoRA adapter의 local path를 알고 있어야 합니다.

## 실행

`.env`를 설정합니다.

```env
ENABLE_LORA=true
LORA_MODULE_NAME=my-adapter
LORA_MODULE_PATH=/path/to/local/adapter
```

설정을 확인합니다.

```bash
uv run python scripts/run_lora_test.py
```

## 성공 확인

`LORA_MODULE_NAME`과 `LORA_MODULE_PATH`가 출력되면 설정 확인은 성공입니다.

그 다음 vLLM을 LoRA 지원 옵션과 함께 시작하고 같은 client를 호출합니다.

```bash
uv run python scripts/call_chat.py
```

## 자주 막히는 지점

adapter path가 비어 있으면 script가 실패합니다. `.env`의 `LORA_MODULE_PATH`가 실제 local 경로인지 확인하세요.

## 다음 챕터

[실습 8: Speculative decoding](08_speculative_decoding.md)
