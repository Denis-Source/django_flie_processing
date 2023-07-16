from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import settings
from task.models import Task
from task.on_demand import test_task
from api.v1.task.serializers import TaskCreateSerializer

class StartTaskView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TaskCreateSerializer
    @swagger_auto_schema(
        responses={
            201: "Task created successfully",
            400: "Bad data"})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get("name")

        task = Task(name=name, initiator=self.request.user)
        task.save()

        test_task.apply_async(args=[task.id], soft_time_limit=settings.STALE_TASK_AGE)
        return Response()
