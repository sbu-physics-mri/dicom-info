"""Custom exception classes for dicominfo."""


class DicomReadError(Exception):
    """Raised when DICOM files cannot be read."""


class NoPixelDataError(Exception):
    """Raised when no DICOM files contain pixel data."""
