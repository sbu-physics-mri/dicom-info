"""Allow running dicominfo as a module with python -m dicominfo."""
# pragma: no cover

from dicominfo.cli import main

if __name__ == "__main__":
    main()
