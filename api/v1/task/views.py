from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import settings
from task.models import Task
from task.on_demand import test_task


class StartTaskView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        task = Task(name="test_task", initiator=self.request.user)
        task.save()

        test_task.apply_async(args=[task.id], soft_time_limit=settings.STALE_TASK_AGE)
        return Response()
