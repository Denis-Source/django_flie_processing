from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from api.v1.task.filters import TaskFilter
from api.v1.task.paginations import TaskPagination
from api.v1.task.serializers import TaskSerializer, DocumentConversionTaskSerializer
from core import settings
from task.document.services import convert_file
from task.models import Task, DocumentConversionTask
from task.document.tasks import convert_document

class ListHistoryTasks(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    pagination_class = TaskPagination

    def get_queryset(self):
        return Task.get_closed_tasks().filter(initiator=self.request.user)

    @swagger_auto_schema(
        responses={
            200: "List of closed tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListOpenedTasks(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.get_opened_tasks().filter(initiator=self.request.user)

    @swagger_auto_schema(
        responses={
            200: "List of opened tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """List opened tasks and their maximum acceptable amount"""
        return super().get(request, *args, **kwargs)


class CreateDocumentConversionTaskView(CreateAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = DocumentConversionTaskSerializer
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        task = DocumentConversionTask.objects.create(
            initiator=self.request.user,
            name=serializer.validated_data.get("name"),
            input_file=serializer.validated_data.get("input_file"),
            output_format=serializer.validated_data.get("output_format"))
        convert_document.apply_async(
            soft_time_limit=settings.STALE_TASK_AGE,
            kwargs={"task_id": task.id})

    @swagger_auto_schema(
        responses={
            201: DocumentConversionTaskSerializer,
            400: "Bad request",
            401: "Unauthorized"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
