import sys

from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    sys.argv = ["daphne", "core.asgi:application"]
    CommandLineInterface.entrypoint()
