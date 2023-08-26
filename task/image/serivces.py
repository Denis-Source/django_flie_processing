import os
from os import makedirs
from pathlib import Path

from PIL import Image
from django.core.files.base import File

from core import settings
from task.image.constants import COLOR_MODES
from task.models import ConversionTask


def convert_path(input_path: str, output_path: str, quality=100):
    """Convert image using paths (strings)"""
    image = Image.open(input_path)
    frmt = Path(output_path).suffix.replace(".", "")
    expected_mode = COLOR_MODES[frmt]
    if not expected_mode == image.mode:
        image = image.convert(expected_mode)
    image.save(output_path, quality=quality)


def convert_file(input_file: File, frmt: str, output_file=None, quality=100):
    """
    Convert image using django files

    Creates a new file if output file is not specified
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

    convert_path(os.path.join(settings.MEDIA_ROOT, input_file.name), output_file.name, quality)
    output_file.name = output_file.name.replace(f"{settings.MEDIA_ROOT}/", "")
    return output_file
