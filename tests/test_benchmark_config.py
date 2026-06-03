from pathlib import Path

from types import SimpleNamespace

from vllm_lab.benchmark import BenchmarkResult, run_benchmark, write_markdown
from vllm_lab.config import Settings
from vllm_lab.prompts import get_prompt


def test_get_prompt_uses_config_file(tmp_path: Path):
    config = tmp_path / "prompts.toml"
    config.write_text('[prompts]\nshort = "hello from config"\n', encoding="utf-8")

    assert get_prompt("short", config) == "hello from config"


def test_write_markdown_uses_simple_beginner_table(tmp_path: Path):
    output = tmp_path / "latest.md"
    write_markdown(
        [
            BenchmarkResult(
                model_profile="tiny",
                model="Qwen/Qwen2.5-0.5B-Instruct",
                max_tokens=64,
                prompt_preset="short",
                request_rate=1,
                prefix_cache=False,
                avg_latency_seconds=0.5,
                throughput_tokens_per_second=12.3,
                completed_requests=1,
            )
        ],
        output,
    )

    text = output.read_text(encoding="utf-8")
    assert "| Model Profile | Max Tokens | Prompt Preset |" in text
    assert "| tiny | 64 | short | 1 | false | 0.500s | 12.30 tok/s |  |" in text


def test_run_benchmark_uses_config_without_real_server():
    class FakeCompletions:
        def create(self, **kwargs):
            return SimpleNamespace(usage=SimpleNamespace(completion_tokens=7))

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
    config = Settings(
        benchmark_num_prompts=3,
        benchmark_request_rate=0,
        benchmark_max_concurrency=2,
        default_model="test-model",
        default_max_tokens=16,
    )

    result = run_benchmark(config=config, client=fake_client)

    assert result.completed_requests == 3
    assert result.model == "test-model"
    assert result.throughput_tokens_per_second >= 0
