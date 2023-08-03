from django.urls import path

from api.v1.task.document.views import CreateDocumentConversionTaskView, RetrieveDocumentConversionTaskView, \
    RetrieveDocumentFormatsView

FORMATS = "v1-convert-document-formats"
CREATE = "v1-convert-document-create"
RETRIEVE = "v1-convert-document-retrieve"

urlpatterns = [
    path("formats/", RetrieveDocumentFormatsView.as_view(), name=FORMATS),
    path("create/", CreateDocumentConversionTaskView.as_view(), name=CREATE),
    path("<int:id>/", RetrieveDocumentConversionTaskView.as_view(), name=RETRIEVE)
]
