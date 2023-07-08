from django.urls import path

from api.v1.user_auth.views import AuthDetailAPIView, AuthRegisterAPIView, AuthLoginAPIView

urlpatterns = [
    path("profile/", AuthDetailAPIView.as_view(), name="v1-profile"),
    path("register/", AuthRegisterAPIView.as_view(), name="v1-register"),
    path("login/", AuthLoginAPIView.as_view(), name="v1-login"),
]
