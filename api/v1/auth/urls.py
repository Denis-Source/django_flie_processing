from django.urls import path

from api.v1.auth.views import UserDetailAPIView

urlpatterns = [
    path("profile/", UserDetailAPIView.as_view())
]
