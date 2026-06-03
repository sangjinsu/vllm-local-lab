from __future__ import annotations

from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import time

from openai import OpenAI

from vllm_lab.client import create_client
from vllm_lab.config import Settings, settings
from vllm_lab.prompts import get_prompt


@dataclass(frozen=True)
class BenchmarkResult:
    model_profile: str
    model: str
    max_tokens: int
    prompt_preset: str
    request_rate: float
    prefix_cache: bool
    avg_latency_seconds: float
    throughput_tokens_per_second: float
    completed_requests: int
    notes: str = ""


def run_benchmark(
    config: Settings = settings,
    client: OpenAI | None = None,
    num_prompts: int | None = None,
    prompt_preset: str | None = None,
    max_tokens: int | None = None,
    request_rate: float | None = None,
    max_concurrency: int | None = None,
    prefix_cache: bool | None = None,
) -> BenchmarkResult:
    active_client = client or create_client(config)
    active_num_prompts = num_prompts or config.benchmark_num_prompts
    active_prompt_preset = prompt_preset or config.benchmark_prompt_preset
    active_max_tokens = max_tokens or config.default_max_tokens
    active_request_rate = request_rate or config.benchmark_request_rate
    active_max_concurrency = max(1, max_concurrency or config.benchmark_max_concurrency)
    active_prefix_cache = config.enable_prefix_caching if prefix_cache is None else prefix_cache
    prompt = get_prompt(active_prompt_preset)

    latencies: list[float] = []
    generated_tokens = 0
    delay_seconds = 1 / active_request_rate if active_request_rate > 0 else 0

    def send_request(index: int) -> tuple[float, int]:
        started = time.perf_counter()
        response = active_client.chat.completions.create(
            model=config.default_model,
            messages=[{"role": "user", "content": f"{prompt}\n\nRun: {index + 1}"}],
            temperature=config.default_temperature,
            top_p=config.default_top_p,
            max_tokens=active_max_tokens,
        )
        elapsed = time.perf_counter() - started
        usage = getattr(response, "usage", None)
        completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        return elapsed, completion_tokens

    with ThreadPoolExecutor(max_workers=active_max_concurrency) as executor:
        futures = []
        for index in range(active_num_prompts):
            futures.append(executor.submit(send_request, index))
            if delay_seconds > 0 and index < active_num_prompts - 1:
                time.sleep(delay_seconds)

        for future in as_completed(futures):
            elapsed, completion_tokens = future.result()
            latencies.append(elapsed)
            generated_tokens += completion_tokens

    total_latency = sum(latencies)
    avg_latency = total_latency / len(latencies) if latencies else 0.0
    throughput = generated_tokens / total_latency if total_latency > 0 else 0.0

    return BenchmarkResult(
        model_profile=config.model_profile,
        model=config.default_model,
        max_tokens=active_max_tokens,
        prompt_preset=active_prompt_preset,
        request_rate=active_request_rate,
        prefix_cache=active_prefix_cache,
        avg_latency_seconds=avg_latency,
        throughput_tokens_per_second=throughput,
        completed_requests=len(latencies),
        notes="",
    )


def write_csv(results: list[BenchmarkResult], path: Path | str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(_result_row(results[0] if results else _empty_result()).keys()))
        writer.writeheader()
        for result in results:
            writer.writerow(_result_row(result))


def write_markdown(results: list[BenchmarkResult], path: Path | str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "| Model Profile | Max Tokens | Prompt Preset | Request Rate | Prefix Cache | Avg Latency | Throughput | Notes |",
        "|---|---:|---|---:|---|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            "| "
            f"{result.model_profile} | "
            f"{result.max_tokens} | "
            f"{result.prompt_preset} | "
            f"{result.request_rate:g} | "
            f"{str(result.prefix_cache).lower()} | "
            f"{result.avg_latency_seconds:.3f}s | "
            f"{result.throughput_tokens_per_second:.2f} tok/s | "
            f"{result.notes} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _result_row(result: BenchmarkResult) -> dict[str, str | int | float | bool]:
    return {
        "model_profile": result.model_profile,
        "model": result.model,
        "max_tokens": result.max_tokens,
        "prompt_preset": result.prompt_preset,
        "request_rate": result.request_rate,
        "prefix_cache": result.prefix_cache,
        "avg_latency_seconds": round(result.avg_latency_seconds, 6),
        "throughput_tokens_per_second": round(result.throughput_tokens_per_second, 6),
        "completed_requests": result.completed_requests,
        "notes": result.notes,
    }


def _empty_result() -> BenchmarkResult:
    return BenchmarkResult("", "", 0, "", 0.0, False, 0.0, 0.0, 0)
