from api.views.get_learning_units import get_learning_goals

from django.urls import path

urlpatterns = [
    path('learning-goals/', get_learning_goals),
]
