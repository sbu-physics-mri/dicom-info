"""dicom-info package - Version and exports."""

__version__ = "0.2.0"

# Export main entry point
from dicominfo.cli import main

# Export core functions for library use
from dicominfo.core import print_stats

# Export exception classes
from dicominfo.exceptions import DicomReadError, NoPixelDataError


def __getattr__(name):
    """Lazy import display_images to avoid loading matplotlib unless needed."""
    if name == "display_images":
        from dicominfo.viewer import display_images
        return display_images
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "main",
    "print_stats",
    "display_images",
    "DicomReadError",
    "NoPixelDataError",
    "__version__",
]
