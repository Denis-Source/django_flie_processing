from django.urls import path

from api.v1.upload.views import CreateUploadView, RetrieveUploadView, ListUploadView

CREATE = "v1-upload-create"
RETRIEVE = "v1-upload-retrieve"
LIST = "v1-upload-list"

urlpatterns = [
    path("create/", CreateUploadView.as_view(), name=CREATE),
    path("<str:id>/", RetrieveUploadView.as_view(), name=RETRIEVE),
    path("", ListUploadView.as_view(), name=LIST)
]
