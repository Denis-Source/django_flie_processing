from django.urls import path

from api.v1.task.views import StartTaskView

urlpatterns = [
    path("", StartTaskView.as_view()),
]
