import os
from pathlib import Path

from PIL import Image
from django.core.files import File
from pytesseract import image_to_string

from core import settings


def get_text_from_path(input_path: str, languages: list[str] = ["eng"]) -> str:
    """
    Get text from image

    If no language is specified, defaults to english
    """
    if not languages:
        languages = []

    trained_data_path = str(settings.BASE_DIR.joinpath("task/ocr/traneddata"))
    return image_to_string(Image.open(input_path),
                           config=f"--tessdata-dir {trained_data_path} -l {'+'.join(languages)}")


def get_text_from_file(input_file: File, languages: list[str] = ["eng"]) -> str:
    """
    Get text from django file
    """
    input_path = Path(input_file.name)
    output = get_text_from_path(os.path.join(settings.MEDIA_ROOT, input_path.name), languages=languages)
    return output
