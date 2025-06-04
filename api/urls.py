from django.urls import path
from api.endpoints.list_learning_goals_for_language import ListLearningGoalsForLanguageView
from api.endpoints.list_units_of_meaning_for_learning_goal import list_units_of_meaning_for_learning_goal

urlpatterns = [
    path('list_learning_goals_for_language/<str:language_code>/', ListLearningGoalsForLanguageView.as_view(), name='list_learning_goals_for_language'),
    path('list_units_of_meaning_for_learning_goal/<int:learning_goal_id>/', list_units_of_meaning_for_learning_goal, name='list_units_of_meaning_for_learning_goal'),
]