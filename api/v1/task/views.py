from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.task.filters import TaskFilter
from api.v1.task.paginations import TaskPagination
from api.v1.task.permisions import IsNotExceededOpenTasks
from api.v1.task.serializers import TaskSerializer
from core import settings
from task.models import Task, ConversionTask


class ListHistoryTasks(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    pagination_class = TaskPagination

    def get_queryset(self):
        """Get tasks that are initiated by the requested user"""
        return Task.get_closed_tasks().filter(initiator=self.request.user)

    @swagger_auto_schema(
        tags=["Task", ],
        responses={
            200: "List of closed tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """Return paginated filtered list of tasks, created by the requested user"""
        return super().get(request, *args, **kwargs)


class ListOpenedTasks(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.get_opened_tasks().filter(initiator=self.request.user)

    @swagger_auto_schema(
        tags=["Task", ],
        responses={
            200: "List of opened tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """List opened tasks and their maximum acceptable amount"""
        return super().get(request, *args, **kwargs)


class GenericRetrieveFormatsView(GenericAPIView):
    input_formats = []
    output_formats = []

    def get(self, request):
        """Provides a dictionary of all available input and output formats"""
        return Response({
            "input_formats": self.input_formats,
            "output_formats": self.output_formats,
        })


class CreateConversionTaskView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotExceededOpenTasks]
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser]
    model_class = ConversionTask
    celery_task = None

    def perform_create(self, serializer):
        """
        Create a task and start celery task

        Return an updated serializer with data (created task)
        """
        task = self.model_class.objects.create(
            initiator=self.request.user,
            name=serializer.validated_data.get("name"),
            input_file=serializer.validated_data.get("input_file"),
            output_format=serializer.validated_data.get("output_format"))
        self.celery_task.apply_async(
            soft_time_limit=settings.STALE_TASK_AGE,
            kwargs={"task_id": task.id})
        return self.serializer_class(task)

    def post(self, request, *args, **kwargs):
        """Create a task that will convert an uploaded file into a specified format"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveConversionTaskView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = "id"
    model_class = ConversionTask

    def get_queryset(self):
        return self.model_class.objects.filter(initiator=self.request.user)

    def get(self, request, *args, **kwargs):
        """Retrieve a detail info of a task with a specified id"""
        return super().get(request, *args, **kwargs)
