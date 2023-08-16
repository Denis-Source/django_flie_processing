from drf_yasg.utils import swagger_auto_schema

from api.v1.task.image.serializers import ImageConversionTaskSerializer
from api.v1.task.views import GenericRetrieveFormatsView, CreateConversionTaskView, \
    RetrieveConversionTaskView
from core import settings
from core.constants import IMAGE_OUTPUT_FORMATS, IMAGE_INPUT_FORMATS
from task.image.tasks import convert_image
from task.models import ImageConversionTask


class RetrieveImageFormatsView(GenericRetrieveFormatsView):
    tags = ["Image"]
    input_formats = IMAGE_INPUT_FORMATS
    output_formats = IMAGE_OUTPUT_FORMATS

    @swagger_auto_schema(
        tags=tags,
        responses={
            200: "Dictionary of all available formats and their names"})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateImageConversionTaskView(CreateConversionTaskView):
    model_class = ImageConversionTask
    serializer_class = ImageConversionTaskSerializer
    celery_task = convert_image

    def perform_create(self, serializer):
        task = self.model_class.objects.create(
            initiator=self.request.user,
            name=serializer.validated_data.get("name"),
            input_file=serializer.validated_data.get("input_file"),
            output_format=serializer.validated_data.get("output_format"),
            quality=serializer.validated_data.get("quality"))
        self.celery_task.apply_async(
            soft_time_limit=settings.STALE_TASK_AGE,
            kwargs={"task_id": task.id})
        return self.serializer_class(task)

    @swagger_auto_schema(
        tags=["Image"],
        responses={
            201: ImageConversionTaskSerializer,
            400: "Bad request",
            401: "Unauthorized"})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RetrieveImageConversionTaskView(RetrieveConversionTaskView):
    serializer_class = ImageConversionTaskSerializer
    model_class = ImageConversionTask

    @swagger_auto_schema(
        tags=["Image"],
        responses={
            200: ImageConversionTaskSerializer,
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
