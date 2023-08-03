from django.urls import path

from api.v1.clipboard.views import CreateClipBoardView, RetrieveClipBoardView, ListClipBoardView

urlpatterns = [
    path("create/", CreateClipBoardView.as_view(), name="v1-clipboard-create"),
    path("<int:id>/", RetrieveClipBoardView.as_view(), name="v1-clipboard-retrieve"),
    path("", ListClipBoardView.as_view(), name="v1-clipboard-list")
]
