import os

from PIL import Image
from pytesseract import image_to_string

from core import settings


def get_text_from_image(input_path: str, languages: list[str] = ["eng"]) -> str:
    if not languages:
        languages = []

    trained_data_path = str(settings.BASE_DIR.joinpath("task/ocr/traneddata"))
    return image_to_string(Image.open(input_path), config=f"--tessdata-dir {trained_data_path} -l {'+'.join(languages)}")
