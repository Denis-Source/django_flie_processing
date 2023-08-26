from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.task.filters import TaskFilter
from api.v1.task.paginations import TaskPagination
from api.v1.task.permisions import IsNotExceededOpenTasks
from api.v1.task.serializers import ConversionTaskSerializer, CreateConversionTaskSerializer
from core import settings
from core.constants import IMAGE_INPUT_FORMATS, IMAGE_OUTPUT_FORMATS, DOCUMENT_INPUT_FORMATS, DOCUMENT_OUTPUT_FORMATS
from task.document.tasks import convert_document
from task.image.tasks import convert_image
from task.models import ConversionTask
from upload.models import Upload


class ListHistoryConversionTasks(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversionTaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    pagination_class = TaskPagination

    def get_queryset(self):
        """Get tasks that are initiated by the requested user"""
        return ConversionTask.get_closed_tasks().filter(initiator=self.request.user).order_by("-created_at")

    @swagger_auto_schema(
        tags=["Task"],
        responses={
            200: "List of closed tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """Return paginated filtered list of tasks, created by the requested user"""
        return super().get(request, *args, **kwargs)


class ListOpenedConversionTasks(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversionTaskSerializer

    def get_queryset(self):
        return ConversionTask.get_opened_tasks().filter(initiator=self.request.user).order_by("-created_at")

    @swagger_auto_schema(
        tags=["Task"],
        responses={
            200: "List of opened tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """List opened tasks and their maximum acceptable amount"""
        return super().get(request, *args, **kwargs)


class RetrieveConversionFormatsView(GenericAPIView):
    @swagger_auto_schema(
        tags=["Task"],
        responses={
            200: "List of available formats",
            401: "Unauthorized"})
    def get(self, request):
        """Provides a dictionary of all available input and output formats for media types"""
        return Response({
            Upload.MediaTypes.IMAGE: {
                "input_formats": IMAGE_INPUT_FORMATS,
                "output_formats": IMAGE_OUTPUT_FORMATS
            },
            Upload.MediaTypes.DOCUMENT: {
                "input_formats": DOCUMENT_INPUT_FORMATS,
                "output_formats": DOCUMENT_OUTPUT_FORMATS
            }
        })


class CreateConversionTaskView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotExceededOpenTasks]
    serializer_class = CreateConversionTaskSerializer

    def get_celery_task(self, task: ConversionTask):
        match task.upload.media_type:
            case Upload.MediaTypes.IMAGE:
                return convert_image
            case Upload.MediaTypes.VIDEO:
                return None
            case Upload.MediaTypes.DOCUMENT:
                return convert_document
            case Upload.MediaTypes.OTHER:
                return None

    def perform_create(self, serializer):
        """
        Create a task and start celery task

        Return an updated serializer with data (created task)
        """
        task = ConversionTask.objects.create(
            initiator=self.request.user,
            name=serializer.validated_data.get("name"),
            upload=serializer.validated_data.get("upload"),
            output_format=serializer.validated_data.get("output_format"),
            quality=serializer.validated_data.get("quality")
        )
        celery_task = self.get_celery_task(task)
        celery_task.apply_async(
            soft_time_limit=settings.STALE_TASK_AGE,
            kwargs={"task_id": task.id})
        return ConversionTaskSerializer(task)

    @swagger_auto_schema(
        tags=["Task"],
        responses={
            201: ConversionTaskSerializer,
            401: "Unauthorized"})
    def post(self, request, *args, **kwargs):
        """Create a task that will convert an uploaded file into a specified format"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveConversionTaskView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    model_class = ConversionTask
    serializer_class = ConversionTaskSerializer

    def get_queryset(self):
        return self.model_class.objects.filter(initiator=self.request.user)

    @swagger_auto_schema(
        tags=["Task"],
        responses={
            200: ConversionTaskSerializer,
            401: "Unauthorized"})   
    def get(self, request, *args, **kwargs):
        """Retrieve a detail info of a task with a specified id"""
        return super().get(request, *args, **kwargs)
