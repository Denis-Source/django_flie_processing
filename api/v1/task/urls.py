from django.urls import path, include

urlpatterns = [
    path("conversion/", include("api.v1.task.conversion.urls")),
    path("ocr/", include("api.v1.task.ocr.urls"))
]
