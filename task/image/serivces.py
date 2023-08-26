import os
from os import makedirs
from pathlib import Path

from PIL import Image
from django.core.files.base import File
from django.utils.timezone import now

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


def convert_file(input_file: File, frmt: str, quality=100):
    """
    Convert image using django files

    Creates a new file if output file is not specified
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
        os.path.join(settings.MEDIA_ROOT, ConversionTask.OUTPUT_FOLDER, output_path.name),
        quality)
    output_file.name = os.path.join(ConversionTask.OUTPUT_FOLDER, output_path.name)
    return output_file
