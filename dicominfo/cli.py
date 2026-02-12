"""CLI argument parsing and main entry point."""

import argparse
import sys

from dicominfo.core import print_stats
from dicominfo.exceptions import DicomReadError, NoPixelDataError


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

        # Display images - import viewer only if needed
        if args.display:
            from dicominfo.viewer import display_images
            display_images(args.file, max_cols=args.columns)

    except (DicomReadError, NoPixelDataError) as err:
        print(err)
        sys.exit(1)
