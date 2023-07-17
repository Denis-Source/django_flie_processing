from django.urls import path

from api.v1.task.views import StartGenerationCreationView, AlgorithmChoicesView, ListOpenedTasks, ListHistoryTasks

urlpatterns = [
    path("history", ListHistoryTasks.as_view(), name="v1-task-history"),
    path("opened", ListOpenedTasks.as_view(), name="v1-task-opened"),
    path("maze_generate", StartGenerationCreationView.as_view(), name="v1-maze-generate"),
    path("maze_alogrithms", AlgorithmChoicesView.as_view(), name="v1-maze-algorithms"),
]
