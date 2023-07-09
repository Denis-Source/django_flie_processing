import sys

if __name__ == "__main__":
    sys.argv = ["daphne", "core.asgi:application"]
    from daphne.cli import CommandLineInterface

    CommandLineInterface.entrypoint()
