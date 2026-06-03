from openai import OpenAIError

from vllm_lab.benchmark_matrix import run_benchmark_matrix, write_latest_reports


def main() -> None:
    try:
        results = run_benchmark_matrix()
    except OpenAIError as exc:
        print(f"Benchmark matrix request가 실패했습니다: {exc}")
        print("local server를 먼저 시작하세요. 실행: uv run python scripts/local_serve_help.py")
        raise SystemExit(1) from exc

    csv_path, markdown_path = write_latest_reports(results)
    print(f"Benchmark matrix report를 생성했습니다: {csv_path}, {markdown_path}")


if __name__ == "__main__":
    main()
