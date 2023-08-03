from django.urls import path

from api.v1.user_auth.views import AuthDetailAPIView, AuthRegisterAPIView, AuthLoginAPIView

PROFILE = "v1-profile"
REGISTER = "v1-register"
LOGIN = "v1-login"

urlpatterns = [
    path("profile/", AuthDetailAPIView.as_view(), name=PROFILE),
    path("register/", AuthRegisterAPIView.as_view(), name=REGISTER),
    path("login/", AuthLoginAPIView.as_view(), name=LOGIN),
]
