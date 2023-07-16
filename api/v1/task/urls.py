from django.urls import path

from api.v1.task.views import StartGenerationCreationView, AlgorithmChoicesView

urlpatterns = [
    path("maze_generate", StartGenerationCreationView.as_view()),
    path("maze_alogrithms", AlgorithmChoicesView.as_view()),
]
