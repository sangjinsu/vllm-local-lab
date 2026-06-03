from vllm_lab.config import settings


def main() -> None:
    if not settings.enable_speculative_decoding:
        print("ENABLE_SPECULATIVE_DECODING=false")
        print("Speculative decoding을 테스트하기 전에 ENABLE_SPECULATIVE_DECODING=true와 SPECULATIVE_CONFIG_JSON을 설정하세요.")
        return
    if not settings.speculative_config_json:
        print("SPECULATIVE_CONFIG_JSON이 비어 있습니다.")
        raise SystemExit(1)

    print("다음 speculative config로 vLLM을 다시 시작하세요:")
    print(settings.speculative_config_json)
    print("그 다음 실행: uv run python scripts/run_benchmark.py")


if __name__ == "__main__":
    main()
