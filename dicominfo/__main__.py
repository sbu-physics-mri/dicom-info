"""Allow running dicominfo as a module with python -m dicominfo."""

from dicominfo.cli import main  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    main()
