from vllm_lab.health import check_health, list_models


def main() -> None:
    health = check_health()
    print(f"{health.endpoint}: {health.message}")
    if not health.ok:
        raise SystemExit(1)

    models = list_models()
    print(f"{models.endpoint}: {models.message}")
    if not models.ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
