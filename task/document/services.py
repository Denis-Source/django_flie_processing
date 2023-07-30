import os.path
from os import makedirs
from pathlib import Path
from pypandoc import convert_file as convert_pandoc_path
from django.core.files.base import ContentFile, File

from core import settings
from task.document.constants import OUTPUT_FORMATS
from task.models import DocumentConversionTask


def convert_path(input_path: str, frmt: str, output_path: str):
    convert_pandoc_path(input_path, frmt, outputfile=output_path)

def convert_file(input_file: File, frmt: str, output_file=None):
    # TODO properly close a file
    input_path = Path(input_file.name)

    if not output_file:
        output_path = Path(
            settings.MEDIA_ROOT,
            DocumentConversionTask.OUTPUT_FOLDER,
            f"{input_path.stem}.{frmt}"
        )
        makedirs(output_path.parent, exist_ok=True)
        output_file = File(open(output_path, "wb"))

    convert_path(os.path.join(settings.MEDIA_ROOT, input_file.name), OUTPUT_FORMATS[frmt], output_file.name)
    output_file.name = output_file.name.replace(f"{settings.MEDIA_ROOT}/", "")
    return output_file

