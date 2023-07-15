import sys

from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    sys.argv = ["daphne", "core.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
    CommandLineInterface.entrypoint()
