from vllm_lab.config import settings


def main() -> None:
    try:
        from vllm import LLM, SamplingParams
    except ImportError as exc:
        print("현재 환경에 vLLM package가 설치되어 있지 않습니다.")
        print("환경에 맞게 설치하거나 실행하세요: uv sync --extra serve")
        raise SystemExit(1) from exc

    llm = LLM(model=settings.default_model, dtype=settings.default_dtype)
    params = SamplingParams(
        temperature=settings.default_temperature,
        top_p=settings.default_top_p,
        max_tokens=settings.default_max_tokens,
    )
    outputs = llm.generate(["Explain vLLM in one simple sentence."], params)
    print(outputs[0].outputs[0].text)


if __name__ == "__main__":
    main()
