from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REQUIRED_ADAPTER_FILES = ("adapter_config.json", "adapter_model.safetensors")
PLACEHOLDER_SAFETENSORS_MAX_BYTES = 16


@dataclass(frozen=True)
class LoraAdapterCheck:
    path: Path
    path_exists: bool
    files: dict[str, bool]
    safetensors_size_bytes: int | None

    @property
    def missing_files(self) -> list[str]:
        return [name for name, exists in self.files.items() if not exists]

    @property
    def has_required_files(self) -> bool:
        return self.path_exists and not self.missing_files

    @property
    def looks_like_placeholder(self) -> bool:
        if self.safetensors_size_bytes is None:
            return False
        return self.safetensors_size_bytes <= PLACEHOLDER_SAFETENSORS_MAX_BYTES


def check_lora_adapter_path(path: str | Path) -> LoraAdapterCheck:
    adapter_path = Path(path).expanduser()
    files = {
        file_name: (adapter_path / file_name).is_file()
        for file_name in REQUIRED_ADAPTER_FILES
    }

    safetensors_path = adapter_path / "adapter_model.safetensors"
    safetensors_size = safetensors_path.stat().st_size if safetensors_path.is_file() else None

    return LoraAdapterCheck(
        path=adapter_path,
        path_exists=adapter_path.is_dir(),
        files=files,
        safetensors_size_bytes=safetensors_size,
    )
