from django.urls import path

from api.v1.task.views import ListOpenedTasks, ListHistoryTasks

urlpatterns = [
    path("history", ListHistoryTasks.as_view(), name="v1-task-history"),
    path("opened", ListOpenedTasks.as_view(), name="v1-task-opened"),
]
