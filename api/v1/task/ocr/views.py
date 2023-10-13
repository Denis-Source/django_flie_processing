from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.task.ocr.filters import OCRFilter
from api.v1.task.ocr.serializers import CreateOCRTaskSerializer, OCRTaskSerializer
from api.v1.task.paginations import TaskPagination
from api.v1.task.permisions import IsNotExceededOpenTasks
from task.models import OCRTask


class ListHistoryOCRTasksView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OCRTaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OCRFilter
    pagination_class = TaskPagination

    def get_queryset(self):
        """Get ocr tasks that are initiated by the requested user"""
        return OCRTask.get_closed_tasks().filter(initiator=self.request.user).order_by("-created_at")

    @swagger_auto_schema(
        tags=["OCR"],
        responses={
            200: "List of closed OCR tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """Return paginated filtered list of OCR tasks, created by the requested user"""
        return super().get(request, *args, **kwargs)


class ListOpenedOCRTasksView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OCRTaskSerializer

    def get_queryset(self):
        return OCRTask.get_opened_tasks().filter(initiator=self.request.user).order_by("-created_at")

    @swagger_auto_schema(
        tags=["OCR"],
        responses={
            200: "List of opened OCR tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """List opened OCR tasks and their maximum acceptable amount"""
        return super().get(request, *args, **kwargs)


class CreateOCRTaskView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotExceededOpenTasks]
    serializer_class = CreateOCRTaskSerializer

    def perform_create(self, serializer):
        task = OCRTask.objects.create(
            initiator=self.request.user,
            name=serializer.validated_data.get("name"),
            language=serializer.validated_data.get("language"),
            upload=serializer.validated_data.get("upload")
        )
        return OCRTaskSerializer(task)

    @swagger_auto_schema(
        tags=["OCR"],
        responses={
            201: OCRTaskSerializer,
            401: "Unauthorized, Limit Exceeded"})
    def post(self, request, *args, **kwargs):
        """Create an OCR task that will recognize text from uploaded image with specified language"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveOCRTaskView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    serializer_class = OCRTaskSerializer

    def get_queryset(self):
        return OCRTask.objects.filter(initiator=self.request.user)

    @swagger_auto_schema(
        tags=["OCR"],
        responses={
            200: OCRTaskSerializer,
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """Retrieve a detail info of an OCR task with a specified id"""
        return super().get(request, *args, **kwargs)


class RetrieveOCRLanguagesView(GenericAPIView):
    @swagger_auto_schema(
        tags=["OCR"],
        responses={
            200: "List of available languages"})
    def get(self, request):
        """Provides a dictionary of all available languages for OCR"""
        return Response(OCRTask.get_available_languages())
