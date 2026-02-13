"""Single entry point for dicom-info version."""

# Python imports
import importlib.metadata
from pathlib import Path

import tomllib

try:
    __version__ = importlib.metadata.version("dicom-info")
except importlib.metadata.PackageNotFoundError:
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    try:
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        msg = (
            f"Failed to parse {pyproject_path} as TOML"
            " while resolving dicom-info version."
        )
        raise RuntimeError(msg) from exc
    __version__ = data["project"]["version"] + "+dev"
