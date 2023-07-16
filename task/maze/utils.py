import base64
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

IMAGE_FORMAT = "png"

def convert_to_64(image, quality=1):
    """Converts a Pillow image into base64 string"""
    buffer = BytesIO()
    image.save(buffer, format=f"{IMAGE_FORMAT}", quality=quality)
    return base64.b64encode(buffer.getvalue()).decode()


def base64_file(data, name="maze"):
    """Converts a base64 string into a Django file"""
    return ContentFile(base64.b64decode(data), name=f"{name}.{IMAGE_FORMAT}")


def image_to_file(image, name="maze"):
    """Converts a Pillow image into Django Image"""
    buffer = BytesIO()
    image.save(buffer, format=IMAGE_FORMAT)
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=f"{name}.{IMAGE_FORMAT}")
