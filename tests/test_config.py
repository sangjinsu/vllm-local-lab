from vllm_lab.config import Settings, parse_bool, resolve_default_model


def test_resolve_default_model_uses_profile_mapping():
    env = {
        "MODEL_PROFILE": "tiny",
        "MODEL_TINY": "Qwen/Qwen2.5-0.5B-Instruct",
        "MODEL_DEFAULT": "Qwen/Qwen3-0.6B",
    }

    assert resolve_default_model(env["MODEL_PROFILE"], env) == "Qwen/Qwen2.5-0.5B-Instruct"


def test_unknown_profile_falls_back_to_model_default():
    env = {
        "MODEL_PROFILE": "unknown",
        "MODEL_DEFAULT": "Qwen/Qwen3-0.6B",
    }

    assert resolve_default_model(env["MODEL_PROFILE"], env) == "Qwen/Qwen3-0.6B"


def test_settings_reads_benchmark_matrix_values():
    settings = Settings.from_env(
        {
            "BENCHMARK_MODEL_PROFILES": "tiny,default",
            "BENCHMARK_MAX_TOKENS_LIST": "64,128",
            "BENCHMARK_REQUEST_RATE_LIST": "1,2.5",
            "BENCHMARK_PROMPT_PRESET_LIST": "short,long",
            "BENCHMARK_PREFIX_CACHE_LIST": "false,true",
        }
    )

    assert settings.benchmark_model_profiles == ["tiny", "default"]
    assert settings.benchmark_max_tokens_list == [64, 128]
    assert settings.benchmark_request_rate_list == [1.0, 2.5]
    assert settings.benchmark_prompt_preset_list == ["short", "long"]
    assert settings.benchmark_prefix_cache_list == [False, True]


def test_parse_bool_accepts_common_values():
    assert parse_bool("true") is True
    assert parse_bool("0") is False
    assert parse_bool(None, default=True) is True
