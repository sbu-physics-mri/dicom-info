"""CLI entry point for dicom-info."""

# ruff: noqa: T201

from __future__ import annotations

# Python imports
import argparse
import sys

from dicominfo.core import print_stats
from dicominfo.exceptions import DicomInfoError, NoPixelDataError


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Print DICOM file information.",
     )

    parser.add_argument(
        "file",
        help="Path to the DICOM file(s).",
        nargs="+",
        type=str,
    )

    parser.add_argument(
        "-d",
        "--display",
        help="Display DICOM images instead of printing metadata.",
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--columns",
        help="Maximum number of columns for image display.",
        type=int,
        default=None,
    )

    args = parser.parse_args()

    try:
        print_stats(args.file)

        # Display images
        if args.display:
            # Import viewer only when needed
            from dicominfo.viewer import display_images
            display_images(args.file, max_cols=args.columns)

    except NoPixelDataError as err:
        print(f"Error: {err}")
        sys.exit(1)
    except DicomInfoError as err:
        print(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
