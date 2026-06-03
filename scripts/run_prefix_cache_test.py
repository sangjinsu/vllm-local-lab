from vllm_lab.config import settings


def main() -> None:
    if not settings.enable_prefix_caching:
        print("ENABLE_PREFIX_CACHING=false")
        print("ENABLE_PREFIX_CACHING=true로 바꾸고 --enable-prefix-caching으로 vLLM을 다시 시작한 뒤 benchmark를 다시 실행하세요.")
        return

    print(".env에서 prefix caching이 켜져 있습니다.")
    print("실행: uv run python scripts/run_benchmark.py")
    print("그 다음 ENABLE_PREFIX_CACHING=false 실행 결과와 비교하세요.")


if __name__ == "__main__":
    main()
