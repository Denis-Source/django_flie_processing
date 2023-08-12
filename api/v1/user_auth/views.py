from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.v1.user_auth.serializers import UserDetailSerializer, UserCreateSerializer, UserLoginSerializer
from user.models import User


class AuthDetailAPIView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        """Return requested user"""
        return self.request.user

    @swagger_auto_schema(
        tags=["User", ],
        responses={
            200: UserDetailSerializer,
            401: "Unauthenticated"})
    def get(self, request, *args, **kwargs):
        """Return user info"""
        return super().get(request, *args, **kwargs)


class AuthRegisterAPIView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def __init__(self):
        self.obj = None

    def perform_create(self, serializer):
        self.obj = serializer.save()

    @swagger_auto_schema(
        tags=["User", "Registration", ],
        responses={
            201: "User created successfully",
            400: "Bad data"})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
