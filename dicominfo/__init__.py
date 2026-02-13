"""dicom-info package - Version and exports."""

# Python imports
from collections.abc import Callable

# Local imports
from dicominfo._version import __version__
from dicominfo.cli import main
from dicominfo.core import print_stats, validate_files
from dicominfo.exceptions import DicomReadError, NoPixelDataError


def __getattr__(name: str) -> Callable:
    """Lazy import display_images to avoid loading matplotlib unless needed."""
    if name == "display_images":
        from dicominfo.viewer import display_images

        return display_images
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


__all__ = [
    "main",
    "print_stats",
    "validate_files",
    "display_images",  # noqa: F822
    "DicomReadError",
    "NoPixelDataError",
    "__version__",
]
