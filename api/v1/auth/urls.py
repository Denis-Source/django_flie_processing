from django.urls import path

from api.v1.auth.views import AuthDetailAPIView, AuthRegisterAPIView, AuthLoginAPIView, AuthLogoutAPIView

urlpatterns = [
    path("profile/", AuthDetailAPIView.as_view()),
    path("register/", AuthRegisterAPIView.as_view()),
    path("login/", AuthLoginAPIView.as_view()),
    path("logout/", AuthLogoutAPIView.as_view())
]
