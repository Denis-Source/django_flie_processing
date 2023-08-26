import os.path
from os import makedirs
from pathlib import Path

from django.core.files.base import File
from django.utils.timezone import now
from pypandoc import convert_file as convert_pandoc_path

from core import settings
from core.constants import DOCUMENT_OUTPUT_FORMATS
from task.models import ConversionTask


def convert_path(input_path: str, frmt: str, output_path: str):
    """Convert a document to a specified format using path (strings)"""
    convert_pandoc_path(input_path, frmt, outputfile=output_path)


def convert_file(input_file: File, frmt: str):
    """
    Convert a document to a specified format using django files

    Create new file if output file is not specified
    """
    input_path = Path(input_file.name)

    output_path = Path(
        settings.MEDIA_ROOT,
        ConversionTask.OUTPUT_FOLDER,
        f"{input_path.stem}-{round(now().timestamp() * 100)}.{frmt}"
    )
    makedirs(output_path.parent, exist_ok=True)
    output_file = File(open(output_path, "wb").close())

    convert_path(
        os.path.join(settings.MEDIA_ROOT, input_file.name),
        DOCUMENT_OUTPUT_FORMATS[frmt],
        os.path.join(settings.MEDIA_ROOT, ConversionTask.OUTPUT_FOLDER, output_path.name)
    )
    output_file.name = os.path.join(ConversionTask.OUTPUT_FOLDER, output_path.name)
    return output_file
