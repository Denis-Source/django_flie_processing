from django.urls import path, include

from api.v1.task.views import ListOpenedTasks, ListHistoryTasks

HISTORY = "v1-task-history"
OPENED = "v1-task-opened"

urlpatterns = [
    path("history/", ListHistoryTasks.as_view(), name=HISTORY),
    path("opened/", ListOpenedTasks.as_view(), name=OPENED),
    path("document/", include("api.v1.task.document.urls")),
    path("image/", include("api.v1.task.image.urls")),
]
