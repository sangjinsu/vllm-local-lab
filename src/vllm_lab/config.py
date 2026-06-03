from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Mapping

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL_FALLBACK = "Qwen/Qwen3-0.6B"

PROFILE_TO_ENV = {
    "tiny": "MODEL_TINY",
    "default": "MODEL_DEFAULT",
    "small-chat": "MODEL_SMALL_CHAT",
    "balanced": "MODEL_BALANCED",
    "advanced": "MODEL_ADVANCED",
}


def _env_value(env: Mapping[str, str], name: str, default: str) -> str:
    value = env.get(name)
    if value is None or value == "":
        return default
    return value


def parse_bool(value: str | bool | None, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def parse_csv(value: str | None, default: list[str]) -> list[str]:
    if value is None or value.strip() == "":
        return list(default)
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_int_list(value: str | None, default: list[int]) -> list[int]:
    items = parse_csv(value, [str(item) for item in default])
    return [int(item) for item in items]


def parse_float_list(value: str | None, default: list[float]) -> list[float]:
    items = parse_csv(value, [str(item) for item in default])
    return [float(item) for item in items]


def parse_bool_list(value: str | None, default: list[bool]) -> list[bool]:
    items = parse_csv(value, ["true" if item else "false" for item in default])
    return [parse_bool(item) for item in items]


def resolve_default_model(
    profile: str | None = None,
    env: Mapping[str, str] | None = None,
) -> str:
    source = env or os.environ
    selected_profile = profile or source.get("MODEL_PROFILE", "default")
    env_name = PROFILE_TO_ENV.get(selected_profile, "MODEL_DEFAULT")
    return _env_value(source, env_name, _env_value(source, "MODEL_DEFAULT", DEFAULT_MODEL_FALLBACK))


@dataclass(frozen=True)
class Settings:
    lab_env: str = "local"
    log_level: str = "INFO"

    vllm_host: str = "0.0.0.0"
    vllm_port: int = 8000
    vllm_base_url: str = "http://localhost:8000/v1"
    vllm_api_key: str = "EMPTY"

    model_profile: str = "default"
    default_model: str = DEFAULT_MODEL_FALLBACK
    default_tokenizer: str | None = None
    default_dtype: str = "auto"
    default_max_model_len: int = 4096

    hf_token: str | None = None
    hf_home: str = ".cache/huggingface"

    default_temperature: float = 0.7
    default_top_p: float = 0.9
    default_max_tokens: int = 256

    enable_prefix_caching: bool = False
    enable_lora: bool = False
    lora_module_name: str | None = None
    lora_module_path: str | None = None
    enable_speculative_decoding: bool = False
    speculative_config_json: str | None = None

    benchmark_output_dir: str = "results/benchmarks"
    benchmark_num_prompts: int = 20
    benchmark_request_rate: float = 2.0
    benchmark_max_concurrency: int = 4
    benchmark_prompt_preset: str = "short"
    benchmark_result_format: str = "markdown"
    benchmark_model_profiles: list[str] = field(default_factory=lambda: ["tiny", "default"])
    benchmark_max_tokens_list: list[int] = field(default_factory=lambda: [64, 128, 256])
    benchmark_request_rate_list: list[float] = field(default_factory=lambda: [1.0, 2.0, 4.0])
    benchmark_prompt_preset_list: list[str] = field(default_factory=lambda: ["short", "medium", "long"])
    benchmark_prefix_cache_list: list[bool] = field(default_factory=lambda: [False, True])

    docker_image: str = "vllm/vllm-openai:latest"
    docker_container_name: str = "vllm-lab-server"
    docker_port: int = 8000

    k8s_local_runtime: str = "kind"
    k8s_cluster_name: str = "vllm-lab"
    k8s_namespace: str = "vllm-lab"
    k8s_service_name: str = "vllm-server"
    k8s_container_port: int = 8000
    k8s_local_port: int = 8000

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "Settings":
        source = env or os.environ
        profile = source.get("MODEL_PROFILE", "default")
        return cls(
            lab_env=source.get("LAB_ENV", "local"),
            log_level=source.get("LAB_LOG_LEVEL", "INFO"),
            vllm_host=source.get("VLLM_HOST", "0.0.0.0"),
            vllm_port=int(source.get("VLLM_PORT", "8000")),
            vllm_base_url=source.get("VLLM_BASE_URL", "http://localhost:8000/v1"),
            vllm_api_key=source.get("VLLM_API_KEY", "EMPTY"),
            model_profile=profile,
            default_model=resolve_default_model(profile, source),
            default_tokenizer=source.get("DEFAULT_TOKENIZER") or None,
            default_dtype=source.get("DEFAULT_DTYPE", "auto"),
            default_max_model_len=int(source.get("DEFAULT_MAX_MODEL_LEN", "4096")),
            hf_token=source.get("HF_TOKEN") or None,
            hf_home=source.get("HF_HOME", ".cache/huggingface"),
            default_temperature=float(source.get("DEFAULT_TEMPERATURE", "0.7")),
            default_top_p=float(source.get("DEFAULT_TOP_P", "0.9")),
            default_max_tokens=int(source.get("DEFAULT_MAX_TOKENS", "256")),
            enable_prefix_caching=parse_bool(source.get("ENABLE_PREFIX_CACHING"), False),
            enable_lora=parse_bool(source.get("ENABLE_LORA"), False),
            lora_module_name=source.get("LORA_MODULE_NAME") or None,
            lora_module_path=source.get("LORA_MODULE_PATH") or None,
            enable_speculative_decoding=parse_bool(source.get("ENABLE_SPECULATIVE_DECODING"), False),
            speculative_config_json=source.get("SPECULATIVE_CONFIG_JSON") or None,
            benchmark_output_dir=source.get("BENCHMARK_OUTPUT_DIR", "results/benchmarks"),
            benchmark_num_prompts=int(source.get("BENCHMARK_NUM_PROMPTS", "20")),
            benchmark_request_rate=float(source.get("BENCHMARK_REQUEST_RATE", "2")),
            benchmark_max_concurrency=int(source.get("BENCHMARK_MAX_CONCURRENCY", "4")),
            benchmark_prompt_preset=source.get("BENCHMARK_PROMPT_PRESET", "short"),
            benchmark_result_format=source.get("BENCHMARK_RESULT_FORMAT", "markdown"),
            benchmark_model_profiles=parse_csv(source.get("BENCHMARK_MODEL_PROFILES"), ["tiny", "default"]),
            benchmark_max_tokens_list=parse_int_list(source.get("BENCHMARK_MAX_TOKENS_LIST"), [64, 128, 256]),
            benchmark_request_rate_list=parse_float_list(source.get("BENCHMARK_REQUEST_RATE_LIST"), [1.0, 2.0, 4.0]),
            benchmark_prompt_preset_list=parse_csv(
                source.get("BENCHMARK_PROMPT_PRESET_LIST"),
                ["short", "medium", "long"],
            ),
            benchmark_prefix_cache_list=parse_bool_list(source.get("BENCHMARK_PREFIX_CACHE_LIST"), [False, True]),
            docker_image=source.get("DOCKER_IMAGE", "vllm/vllm-openai:latest"),
            docker_container_name=source.get("DOCKER_CONTAINER_NAME", "vllm-lab-server"),
            docker_port=int(source.get("DOCKER_PORT", "8000")),
            k8s_local_runtime=source.get("K8S_LOCAL_RUNTIME", "kind"),
            k8s_cluster_name=source.get("K8S_CLUSTER_NAME", "vllm-lab"),
            k8s_namespace=source.get("K8S_NAMESPACE", "vllm-lab"),
            k8s_service_name=source.get("K8S_SERVICE_NAME", "vllm-server"),
            k8s_container_port=int(source.get("K8S_CONTAINER_PORT", "8000")),
            k8s_local_port=int(source.get("K8S_LOCAL_PORT", "8000")),
        )


settings = Settings.from_env()
