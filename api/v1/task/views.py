from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.task.serializers import MazeCreationTaskGenerationSerializer
from core import settings
from task.models import MazeGenerationTask
from task.on_demand import generate_maze_task


class StartGenerationCreationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = MazeCreationTaskGenerationSerializer

    @swagger_auto_schema(
        responses={
            201: "Task created",
            400: "Bad data",
            401: "Not Authorized"})
    def post(self, request, *args, **kwargs):
        """Generates a maze with the specified parameters
        Starts a celery task and the response will not contain a result"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = MazeGenerationTask(
            name=serializer.validated_data.get("name"),
            initiator=self.request.user,
            width=serializer.validated_data.get("width"),
            height=serializer.validated_data.get("height"),
            algorithm=serializer.validated_data.get("algorithm")
        )
        task.save()

        generate_maze_task.apply_async(args=[task.id], soft_time_limit=settings.STALE_TASK_AGE)
        return Response(status=status.HTTP_201_CREATED)


class AlgorithmChoicesView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        responses={
            200: "List of algorithms"})
    def get(self, request, *args, **kwargs):
        """Lists all available maze generation algorithms"""
        return Response(MazeGenerationTask.ALGORITHMS.choices)
