from django.urls import path, include

from api.v1.task.views import ListHistoryConversionTasksView, ListOpenedConversionTasksView, CreateConversionTaskView, \
    RetrieveConversionTaskView, RetrieveConversionFormatsView

HISTORY = "v1-convert-history"
OPENED = "v1-convert-opened"
CREATE = "v1-convert-create"
RETRIEVE = "v1-convert-retrieve"
FORMATS = "v1-convert-formats"

urlpatterns = [
    path("history/", ListHistoryConversionTasksView.as_view(), name=HISTORY),
    path("opened/", ListOpenedConversionTasksView.as_view(), name=OPENED),
    path("create/", CreateConversionTaskView.as_view(), name=CREATE),
    path("<int:id>/", RetrieveConversionTaskView.as_view(), name=RETRIEVE),
    path("formats/", RetrieveConversionFormatsView.as_view(), name=FORMATS),
    path("ocr/", include("api.v1.task.ocr.urls"))
]
