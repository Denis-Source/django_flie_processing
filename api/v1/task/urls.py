from django.urls import path

from api.v1.task.views import ListOpenedTasks, ListHistoryTasks, CreateDocumentConversionTaskView

urlpatterns = [
    path("history", ListHistoryTasks.as_view(), name="v1-task-history"),
    path("opened", ListOpenedTasks.as_view(), name="v1-task-opened"),
    path("convert-document", CreateDocumentConversionTaskView.as_view(), name="v1-convert-document")
]
