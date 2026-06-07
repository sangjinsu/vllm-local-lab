from vllm_lab.config import settings
from vllm_lab.lora import check_lora_adapter_path


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

    adapter_check = check_lora_adapter_path(settings.lora_module_path)
    if not adapter_check.path_exists:
        print("")
        print("adapter directory를 찾을 수 없습니다.")
        print(f"확인한 경로: {adapter_check.path}")
        raise SystemExit(1)

    print("")
    print("adapter 파일 구조 확인:")
    for file_name, exists in adapter_check.files.items():
        status = "ok" if exists else "missing"
        print(f"- {file_name}: {status}")

    if not adapter_check.has_required_files:
        print("")
        print("필수 adapter 파일이 빠져 있어 실제 LoRA serving을 시작할 수 없습니다.")
        print("adapter_config.json과 adapter_model.safetensors가 있는지 확인하세요.")
        raise SystemExit(1)

    print("")
    print("기본 adapter 파일 구조 확인은 통과했습니다.")

    if adapter_check.looks_like_placeholder:
        print("")
        print("주의: adapter_model.safetensors가 매우 작아 placeholder 파일처럼 보입니다.")
        print("이 파일은 경로와 구조 학습용일 수 있으며, 실제 LoRA weight 여부를 보장하지 않습니다.")
        print("실제 serving은 학습된 adapter 파일로 다시 확인하세요.")

    print("")
    print("실제 adapter가 준비되어 있다면 vLLM server를 --enable-lora와 --lora-modules 옵션으로 시작하세요.")
    print("LoRA adapter를 호출할 때 OpenAI-compatible request의 model 값은 LORA_MODULE_NAME을 사용합니다.")


if __name__ == "__main__":
    main()
