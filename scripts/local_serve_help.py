from vllm_lab.config import settings


def main() -> None:
    command = [
        f"vllm serve {settings.default_model} \\",
        f"  --host {settings.vllm_host} \\",
        f"  --port {settings.vllm_port} \\",
        f"  --dtype {settings.default_dtype} \\",
        f"  --max-model-len {settings.default_max_model_len}",
    ]
    if settings.default_tokenizer:
        command[-1] = f"{command[-1]} \\"
        command.append(f"  --tokenizer {settings.default_tokenizer}")
    if settings.enable_prefix_caching:
        command[-1] = f"{command[-1]} \\"
        command.append("  --enable-prefix-caching")
    print("\n".join(command))


if __name__ == "__main__":
    main()
