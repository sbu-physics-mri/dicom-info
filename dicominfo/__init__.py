"""dicom-info package for reading and displaying DICOM files."""

from __future__ import annotations

# Version
__version__ = "0.2.0"

# Public API exports
from dicominfo.cli import main
from dicominfo.core import print_stats, read_dicom_files
from dicominfo.exceptions import DicomInfoError, DicomReadError, NoPixelDataError

# Optional viewer import (requires matplotlib)
try:
    from dicominfo.viewer import display_images
except ImportError:
    # Matplotlib not available
    display_images = None  # type: ignore[assignment]

__all__ = [
    "__version__",
    "main",
    "print_stats",
    "read_dicom_files",
    "display_images",
    "DicomInfoError",
    "DicomReadError",
    "NoPixelDataError",
]


if __name__ == "__main__":
    main()
