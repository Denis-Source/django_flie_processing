from django.urls import path, include

urlpatterns = [
    path("user_auth/", include("api.v1.user_auth.urls")),
    path("task/", include("api.v1.task.urls")),
    path("upload/", include("api.v1.upload.urls"))
]
