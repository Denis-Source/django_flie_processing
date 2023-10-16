import base64

from django.core.files.base import ContentFile
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.upload.filters import UploadFilter
from api.v1.upload.paginations import UploadPagination
from api.v1.upload.serializers import UploadSerializer, Create64UploadSerializer
from upload.models import Upload
from user.models import User


class Create64UploadView(CreateAPIView):
    serializer_class = Create64UploadSerializer

    def perform_create(self, serializer):
        if isinstance(self.request.user, User):
            user = self.request.user
        else:
            user = None
        base64_content = serializer.validated_data.get("content")
        data, base64_data = base64_content.split(',', 1)
        file_data = base64.b64decode(base64_data)

        upload = Upload.objects.create(
            name=serializer.validated_data.get("name"),
            media_type=serializer.validated_data.get("media_type"),
            file=ContentFile(file_data, name=serializer.validated_data.get("name")),
            user=user,
        )
        return UploadSerializer(upload)

    @swagger_auto_schema(
        tags=["Upload"],
        responses={
            201: UploadSerializer,
            400: "Bad request",
            401: "Unauthorized"})
    def post(self, request, *args, **kwargs):
        """Create an upload from the base64 provided data"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateUploadView(CreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer

    def perform_create(self, serializer):
        """
        Create an upload based on whether the request is authenticated

        Return an upload with user if it is without if it is not
        Return serializer with updated data (created upload)
        """

        if isinstance(self.request.user, User):
            user = self.request.user
        else:
            user = None

        upload = Upload.objects.create(
            name=serializer.validated_data.get("name"),
            media_type=serializer.validated_data.get("media_type"),
            file=serializer.validated_data.get("file"),
            user=user,
        )
        return self.serializer_class(upload)

    @swagger_auto_schema(
        tags=["Upload"],
        responses={
            201: UploadSerializer,
            400: "Bad request",
            401: "Unauthorized"})
    def post(self, request, *args, **kwargs):
        """Create a upload from the provided data"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveUploadView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    serializer_class = UploadSerializer

    def get_queryset(self):
        return Upload.get_users_uploads(self.request.user)

    @swagger_auto_schema(
        tags=["Upload"],
        responses={
            200: UploadSerializer,
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """Return a upload instance with the specified id"""
        return super().get(request, *args, **kwargs)


class ListUploadView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UploadFilter
    pagination_class = UploadPagination

    def get_queryset(self):
        """Return a queryset where upload user is requested user"""
        return Upload.get_users_uploads(self.request.user)

    @swagger_auto_schema(
        tags=["Upload"],
        responses={
            200: UploadSerializer,
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """Retrieve a paginated filtered list of upload instances created by the user"""
        return super().get(request, *args, **kwargs)
