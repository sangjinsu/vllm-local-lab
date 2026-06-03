from vllm_lab.config import settings


def main() -> None:
    if not settings.enable_lora:
        print("ENABLE_LORA=false")
        print("LoRA serving을 시도하기 전에 ENABLE_LORA=true, LORA_MODULE_NAME, LORA_MODULE_PATH를 설정하세요.")
        return
    if not settings.lora_module_name or not settings.lora_module_path:
        print("LoRA는 켜져 있지만 LORA_MODULE_NAME 또는 LORA_MODULE_PATH가 비어 있습니다.")
        raise SystemExit(1)

    print("vLLM을 LoRA 지원 옵션으로 시작할 때 다음 값을 사용하세요:")
    print(f"LORA_MODULE_NAME={settings.lora_module_name}")
    print(f"LORA_MODULE_PATH={settings.lora_module_path}")


if __name__ == "__main__":
    main()
