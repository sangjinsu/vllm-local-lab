from vllm_lab.lora import check_lora_adapter_path


def test_check_lora_adapter_path_reports_missing_directory(tmp_path):
    result = check_lora_adapter_path(tmp_path / "missing-adapter")

    assert result.path_exists is False
    assert result.has_required_files is False
    assert result.missing_files == ["adapter_config.json", "adapter_model.safetensors"]
    assert result.looks_like_placeholder is False


def test_check_lora_adapter_path_detects_required_files_and_placeholder(tmp_path):
    (tmp_path / "adapter_config.json").write_text('{"r": 8}\n', encoding="utf-8")
    (tmp_path / "adapter_model.safetensors").write_bytes(b"\x00" * 10)

    result = check_lora_adapter_path(tmp_path)

    assert result.path_exists is True
    assert result.has_required_files is True
    assert result.missing_files == []
    assert result.safetensors_size_bytes == 10
    assert result.looks_like_placeholder is True
