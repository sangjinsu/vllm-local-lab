import shutil

from vllm_lab.config import settings


def main() -> None:
    serve_command = "vllm serve"
    if settings.disable_flashinfer_sampler:
        serve_command = f"VLLM_USE_FLASHINFER_SAMPLER=0 {serve_command}"

    command = [
        f"{serve_command} {settings.default_model} \\",
        f"  --host {settings.vllm_host} \\",
        f"  --port {settings.vllm_port} \\",
        f"  --dtype {settings.default_dtype} \\",
        f"  --max-model-len {settings.default_max_model_len}",
    ]
    if settings.default_gpu_memory_utilization is not None:
        command[-1] = f"{command[-1]} \\"
        command.append(f"  --gpu-memory-utilization {settings.default_gpu_memory_utilization}")
    if settings.enforce_eager:
        command[-1] = f"{command[-1]} \\"
        command.append("  --enforce-eager")
    if settings.default_tokenizer:
        command[-1] = f"{command[-1]} \\"
        command.append(f"  --tokenizer {settings.default_tokenizer}")
    if settings.enable_prefix_caching:
        command[-1] = f"{command[-1]} \\"
        command.append("  --enable-prefix-caching")
    if settings.enable_lora and settings.lora_module_name and settings.lora_module_path:
        command[-1] = f"{command[-1]} \\"
        command.append("  --enable-lora \\")
        command.append(f"  --lora-modules {settings.lora_module_name}={settings.lora_module_path}")
    print("\n".join(command))

    if not settings.disable_flashinfer_sampler and shutil.which("nvcc") is None:
        print("")
        print("# note: nvcc(CUDA Toolkit)를 찾지 못했습니다.")
        print("# pip wheel로 설치한 vLLM에서는 FlashInfer sampler가 nvcc 없이 커널을 JIT 컴파일하지 못해")
        print("# 모델 로딩 직후 멈출 수 있습니다. 이 경우 .env에 DISABLE_FLASHINFER_SAMPLER=true를 설정하거나")
        print("# WSL에 CUDA Toolkit을 설치하세요. (Windows NVIDIA WSL 환경 참고)")


if __name__ == "__main__":
    main()
