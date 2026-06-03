from __future__ import annotations

from pathlib import Path
import tomllib


DEFAULT_PROMPTS = {
    "short": "Explain vLLM in one simple sentence.",
    "medium": "Explain why an OpenAI-compatible API makes local vLLM experiments easier for a Python learner.",
    "long": (
        "You are helping a beginner learn local LLM serving. Explain the path from starting "
        "a vLLM server to calling it with a Python client, then mention one setting they can change."
    ),
}


def load_prompt_presets(path: Path | str = "configs/prompts.toml") -> dict[str, str]:
    prompt_path = Path(path)
    if not prompt_path.exists():
        return dict(DEFAULT_PROMPTS)

    data = tomllib.loads(prompt_path.read_text(encoding="utf-8"))
    prompts = data.get("prompts", {})
    if not isinstance(prompts, dict):
        return dict(DEFAULT_PROMPTS)

    merged = dict(DEFAULT_PROMPTS)
    for name, value in prompts.items():
        if isinstance(name, str) and isinstance(value, str) and value.strip():
            merged[name] = value
    return merged


def get_prompt(preset: str, path: Path | str = "configs/prompts.toml") -> str:
    prompts = load_prompt_presets(path)
    return prompts.get(preset, prompts["short"])
