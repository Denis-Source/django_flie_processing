from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.clipboard.filters import ClipBoardFilter
from api.v1.clipboard.paginations import ClipBoardPagination
from api.v1.clipboard.serializers import ClipBoardSerializer
from clipboard.models import ClipBoard
from user.models import User


class CreateClipBoardView(CreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = ClipBoardSerializer

    def perform_create(self, serializer):
        """
        Create a clipboard based on whether the request is authenticated

        Return a clipboard with user if it is without if it is not
        Return serializer with updated data (created clipboard)
        """

        if isinstance(self.request.user, User):
            user = self.request.user
        else:
            user = None

        clipboard = ClipBoard.objects.create(
            name=serializer.validated_data.get("name"),
            media_type=serializer.validated_data.get("media_type"),
            file=serializer.validated_data.get("file"),
            auto_delete=serializer.validated_data.get("auto_delete"),
            user=user,
        )
        return self.serializer_class(clipboard)

    @swagger_auto_schema(
        tags=["ClipBoard"],
        responses={
            201: ClipBoardSerializer,
            400: "Bad request",
            401: "Unauthorized"})
    def post(self, request, *args, **kwargs):
        """Create a clipboard from the provided data"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveClipBoardView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    serializer_class = ClipBoardSerializer

    def get_queryset(self):
        return ClipBoard.get_users_clipboard(self.request.user)

    @swagger_auto_schema(
        tags=["ClipBoard"],
        responses={
            200: ClipBoardSerializer,
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """Return a clipboard instance with the specified id"""
        return super().get(request, *args, **kwargs)


class ListClipBoardView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClipBoardSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClipBoardFilter
    pagination_class = ClipBoardPagination

    def get_queryset(self):
        """Return a queryset where clipboard user is requested user"""
        return ClipBoard.get_users_clipboard(self.request.user)

    @swagger_auto_schema(
        tags=["ClipBoard"],
        responses={
            200: ClipBoardSerializer,
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """Retrieve a paginated filtered list of clipboard instances created by the user"""
        return super().get(request, *args, **kwargs)
