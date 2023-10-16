from django.urls import path

from api.v1.upload.views import CreateUploadView, RetrieveUploadView, ListUploadView, Create64UploadView

CREATE = "v1-upload-create"
CREATE_64 = "v1-upload-create64"
RETRIEVE = "v1-upload-retrieve"
LIST = "v1-upload-list"

urlpatterns = [
    path("create/", CreateUploadView.as_view(), name=CREATE),
    path("create64/", Create64UploadView.as_view(), name=CREATE_64),
    path("<str:id>/", RetrieveUploadView.as_view(), name=RETRIEVE),
    path("", ListUploadView.as_view(), name=LIST)
]
