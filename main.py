import subprocess
import sys

from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    command = "python -m celery -A core worker -B -E -l info"
    subprocess.Popen(command, shell=True)

    sys.argv = ["daphne", "core.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
    CommandLineInterface.entrypoint()
