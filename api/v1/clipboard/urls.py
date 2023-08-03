from django.urls import path

from api.v1.clipboard.views import CreateClipBoardView, RetrieveClipBoardView, ListClipBoardView

CREATE = "v1-clipboard-create"
RETRIEVE = "v1-clipboard-retrieve"
LIST = "v1-clipboard-list"

urlpatterns = [
    path("create/", CreateClipBoardView.as_view(), name=CREATE),
    path("<int:id>/", RetrieveClipBoardView.as_view(), name=RETRIEVE),
    path("", ListClipBoardView.as_view(), name=LIST)
]
