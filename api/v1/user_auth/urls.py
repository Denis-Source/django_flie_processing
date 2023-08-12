from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.v1.user_auth.views import AuthDetailAPIView, AuthRegisterAPIView

PROFILE = "v1-profile"
REGISTER = "v1-register"
TOKEN_REFRESH = "v1-token-refresh"
TOKEN_OBTAIN_PAIR = "v1-token-obtain-pair"

urlpatterns = [
    path("profile/", AuthDetailAPIView.as_view(), name=PROFILE),
    path("register/", AuthRegisterAPIView.as_view(), name=REGISTER),
    path('token/', TokenObtainPairView.as_view(), name=TOKEN_OBTAIN_PAIR),
    path('refresh/', TokenRefreshView.as_view(), name=TOKEN_REFRESH),
]
