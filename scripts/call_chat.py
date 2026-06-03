from openai import OpenAIError

from vllm_lab.client import create_client
from vllm_lab.config import settings


def main() -> None:
    client = create_client()
    try:
        response = client.chat.completions.create(
            model=settings.default_model,
            messages=[
                {"role": "user", "content": "Explain vLLM in one simple sentence."}
            ],
            temperature=settings.default_temperature,
            top_p=settings.default_top_p,
            max_tokens=settings.default_max_tokens,
        )
    except OpenAIError as exc:
        print(f"vLLM chat endpoint를 호출할 수 없습니다: {exc}")
        print("local server를 먼저 시작하세요. 실행: uv run python scripts/local_serve_help.py")
        raise SystemExit(1) from exc

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
