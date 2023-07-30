from django.urls import path

from api.v1.task.image.views import RetrieveImageFormatsView, CreateImageConversionTaskView, RetrieveImageConversionTaskView

urlpatterns = [
    path("formats/", RetrieveImageFormatsView.as_view(), name="v1-convert-image-formats"),
    path("create/", CreateImageConversionTaskView.as_view(), name="v1-convert-image-create"),
    path("<int:id>/", RetrieveImageConversionTaskView.as_view(), name="v1-convert-image-retrieve")
]
