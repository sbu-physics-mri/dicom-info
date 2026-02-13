"""CLI argument parsing and main entry point."""

# ruff: noqa: T201

import argparse
import logging
import sys

from dicominfo._version import __version__
from dicominfo.core import print_stats
from dicominfo.exceptions import DicomReadError, NoPixelDataError

logger = logging.getLogger(__name__)


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Print DICOM file information.")

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument("file", help="Path to the DICOM file(s).", nargs="+", type=str)

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

    parser.add_argument(
        "-v", "--verbose", help="Enable debug logging.", action="store_true"
    )

    parser.add_argument(
        "-q",
        "--quiet",
        help="Suppress metadata output (exit codes only).",
        action="store_true",
    )

    args = parser.parse_args()

    # Configure logging based on verbosity flags
    fmt = "%(levelname)s: %(message)s"
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=fmt)
    elif args.quiet:
        logging.basicConfig(level=logging.WARNING, format=fmt)
    else:
        logging.basicConfig(level=logging.INFO, format=fmt)

    # Validate columns argument
    if args.columns is not None and args.columns < 1:
        msg = "--columns must be a positive integer"
        if args.display:
            parser.error(msg)
        else:
            logger.warning("%s. This only applies to the --display flag.", msg)

    try:
        # Only print stats if not in quiet mode
        if not args.quiet:
            print_stats(args.file)
        else:
            # In quiet mode, still need to validate files can be read
            # but don't print the metadata
            from dicominfo.core import validate_files

            validate_files(args.file)

        # Display images - import viewer only if needed
        if args.display:
            from dicominfo.viewer import display_images

            display_images(args.file, max_cols=args.columns)

    except (DicomReadError, NoPixelDataError) as err:
        print(err)
        sys.exit(1)
