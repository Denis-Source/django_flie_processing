from django.urls import path

from api.v1.task.document.views import CreateDocumentConversionTaskView, RetrieveDocumentConversionTaskView, \
    RetrieveDocumentFormatsView

urlpatterns = [
    path("formats/", RetrieveDocumentFormatsView.as_view(), name="v1-convert-document-formats"),
    path("create/", CreateDocumentConversionTaskView.as_view(), name="v1-convert-document-create"),
    path("<int:id>/", RetrieveDocumentConversionTaskView.as_view(), name="v1-convert-document-retrieve")
]
