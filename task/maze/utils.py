import base64
from io import BytesIO

from django.core.files.base import ContentFile


def convert_to_64(image, quality=1):
    buffer = BytesIO()
    image.save(buffer, format="png", quality=quality)
    return base64.b64encode(buffer.getvalue()).decode()


def base64_file(data, name="maze"):
    return ContentFile(base64.b64decode(data), name=f"{name}.png")
