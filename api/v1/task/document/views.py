from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.task.document.serializers import DocumentConversionTaskSerializer
from core import settings
from task.document.tasks import convert_document
from task.models import DocumentConversionTask


class CreateDocumentConversionTaskView(CreateAPIView):
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
        return self.serializer_class(task)

    @swagger_auto_schema(
        responses={
            201: DocumentConversionTaskSerializer,
            400: "Bad request",
            401: "Unauthorized"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class RetrieveDocumentConversionTaskView(RetrieveAPIView):
