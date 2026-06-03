from openai import OpenAIError

from vllm_lab.benchmark import run_benchmark, write_csv, write_markdown
from vllm_lab.config import settings


def main() -> None:
    try:
        result = run_benchmark()
    except OpenAIError as exc:
        print(f"Benchmark request가 실패했습니다: {exc}")
        print("local server를 먼저 시작하세요. 실행: uv run python scripts/local_serve_help.py")
        raise SystemExit(1) from exc

    output_dir = settings.benchmark_output_dir
    write_csv([result], f"{output_dir}/latest.csv")
    write_markdown([result], f"{output_dir}/latest.md")
    print(f"Benchmark report를 생성했습니다: {output_dir}/latest.csv, {output_dir}/latest.md")


if __name__ == "__main__":
    main()
