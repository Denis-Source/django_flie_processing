from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.task.filters import TaskFilter
from api.v1.task.paginations import TaskPagination
from api.v1.task.serializers import TaskSerializer
from task.models import Task


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
        tags=["Task",],
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
        tags=["Task",],
        responses={
            200: "List of opened tasks",
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """List opened tasks and their maximum acceptable amount"""
        return super().get(request, *args, **kwargs)
