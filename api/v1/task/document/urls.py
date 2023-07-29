from django.urls import path

from api.v1.task.document.views import CreateDocumentConversionTaskView
from api.v1.task.views import ListOpenedTasks, ListHistoryTasks

urlpatterns = [
    path("create", CreateDocumentConversionTaskView.as_view(), name="v1-convert-document"),
]
