from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from vllm_lab.benchmark import BenchmarkResult, run_benchmark, write_csv, write_markdown
from vllm_lab.config import Settings, resolve_default_model, settings


def run_benchmark_matrix(config: Settings = settings) -> list[BenchmarkResult]:
    results: list[BenchmarkResult] = []
    for profile in config.benchmark_model_profiles:
        model = resolve_default_model(profile)
        profile_config = replace(config, model_profile=profile, default_model=model)
        for max_tokens in config.benchmark_max_tokens_list:
            for request_rate in config.benchmark_request_rate_list:
                for prompt_preset in config.benchmark_prompt_preset_list:
                    for prefix_cache in config.benchmark_prefix_cache_list:
                        results.append(
                            run_benchmark(
                                profile_config,
                                max_tokens=max_tokens,
                                request_rate=request_rate,
                                prompt_preset=prompt_preset,
                                prefix_cache=prefix_cache,
                            )
                        )
    return results


def write_latest_reports(results: list[BenchmarkResult], config: Settings = settings) -> tuple[Path, Path]:
    output_dir = Path(config.benchmark_output_dir)
    csv_path = output_dir / "latest.csv"
    markdown_path = output_dir / "latest.md"
    write_csv(results, csv_path)
    write_markdown(results, markdown_path)
    return csv_path, markdown_path
