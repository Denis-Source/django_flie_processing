from os import makedirs
from pathlib import Path
from pypandoc import convert_file
from django.core.files.base import ContentFile, File

from core import settings
from task.models import DocumentConversionTask


def convert_paths(input_path: str, frmt: str, output_path: str):
    convert_file(input_path, frmt, outputfile=output_path)

def convert_files(input_file: File, frmt: str, output_file=None):
    # TODO properly close a file
    input_path = Path(input_file.name)

    if not output_file:
        output_path = Path(
            settings.MEDIA_ROOT,
            DocumentConversionTask.OUTPUT_FOLDER,
            f"{input_path.stem}.{frmt}"
        )
        makedirs(output_path.parent, exist_ok=True)
        output_file = File(open(output_path, "w"))


    convert_paths(input_file.name, frmt, output_file.name)
    return output_file

