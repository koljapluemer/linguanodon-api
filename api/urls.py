from django.urls import path
from api.endpoints.list_learning_goals_for_language import ListLearningGoalsForLanguageView

urlpatterns = [
    path('list_learning_goals_for_language/<str:language_code>/', ListLearningGoalsForLanguageView.as_view(), name='list_learning_goals_for_language'),
]