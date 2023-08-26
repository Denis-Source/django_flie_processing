import os.path
from os import makedirs
from pathlib import Path

from django.core.files.base import File
from pypandoc import convert_file as convert_pandoc_path

from core import settings
from core.constants import DOCUMENT_OUTPUT_FORMATS
from task.models import ConversionTask


def convert_path(input_path: str, frmt: str, output_path: str):
    """Convert a document to a specified format using path (strings)"""
    convert_pandoc_path(input_path, frmt, outputfile=output_path)


def convert_file(input_file: File, frmt: str, output_file=None):
    """
    Convert a document to a specified format using django files

    Create new file if output file is not specified
    """
    input_path = Path(input_file.name)

    if not output_file:
        output_path = Path(
            settings.MEDIA_ROOT,
            ConversionTask.OUTPUT_FOLDER,
            f"{input_path.stem}.{frmt}"
        )
        makedirs(output_path.parent, exist_ok=True)
        output_file = File(open(output_path, "wb").close())

    convert_path(os.path.join(settings.MEDIA_ROOT, input_file.name), DOCUMENT_OUTPUT_FORMATS[frmt], output_file.name)
    output_file.name = output_file.name.replace(f"{settings.MEDIA_ROOT}/", "")
    return output_file
