from django.urls import path

from api.v1.task.ocr.views import CreateOCRTaskView, RetrieveOCRTaskView, RetrieveOCRLanguagesView, \
    ListOpenedOCRTasksView, ListHistoryOCRTasksView

HISTORY = "v1-ocr-history"
OPENED = "v1-ocr-opened"
CREATE = "v1-ocr-create"
RETRIEVE = "v1-ocr-retrieve"
LANGUAGES = "v1-ocr-languages"

urlpatterns = [
    path("history/", ListHistoryOCRTasksView.as_view(), name=HISTORY),
    path("opened/", ListOpenedOCRTasksView.as_view(), name=OPENED),
    path("languages/", RetrieveOCRLanguagesView.as_view(), name=LANGUAGES),
    path("create/", CreateOCRTaskView.as_view(), name=CREATE),
    path("<int:id>/", RetrieveOCRTaskView.as_view(), name=RETRIEVE)
]
