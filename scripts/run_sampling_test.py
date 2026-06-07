from openai import OpenAIError

from vllm_lab.client import create_client
from vllm_lab.config import settings


def main() -> None:
    client = create_client()
    prompt = "vLLM is an LLM serving engine. Write one practical reason to run a local vLLM server."
    samples = [
        ("낮은 temperature", 0.2, settings.default_top_p),
        ("기본 temperature", settings.default_temperature, settings.default_top_p),
        ("높은 top_p", settings.default_temperature, min(1.0, settings.default_top_p + 0.1)),
    ]

    for label, temperature, top_p in samples:
        try:
            response = client.chat.completions.create(
                model=settings.default_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                top_p=top_p,
                max_tokens=settings.default_max_tokens,
            )
        except OpenAIError as exc:
            print(f"Sampling request가 실패했습니다: {exc}")
            print("local server를 먼저 시작하세요. 실행: uv run python scripts/local_serve_help.py")
            raise SystemExit(1) from exc

        print(f"\n## {label} (temperature={temperature}, top_p={top_p})")
        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
