from django.urls import path
from api.endpoints.list_learning_goals_for_language import ListLearningGoalsForLanguageView
from api.endpoints.list_learning_goals_for_language_with_min_units import ListLearningGoalsForLanguageWithMinUnitsView
from api.endpoints.list_units_of_meaning_for_learning_goal import list_units_of_meaning_for_learning_goal
from api.endpoints.list_translations_in_language_for_unit_of_meaning import list_translations_in_language_for_unit_of_meaning
from api.endpoints.get_unit_of_meaning import get_unit_of_meaning

urlpatterns = [
    path('list_learning_goals_for_language/<str:language_code>/', ListLearningGoalsForLanguageView.as_view(), name='list_learning_goals_for_language'),
    path('list_learning_goals_for_language_with_min_units/<str:language_code>/', ListLearningGoalsForLanguageWithMinUnitsView.as_view(), name='list_learning_goals_for_language_with_min_units'),
    path('list_units_of_meaning_for_learning_goal/<int:learning_goal_id>/', list_units_of_meaning_for_learning_goal, name='list_units_of_meaning_for_learning_goal'),
    path('list_translations_in_language_for_unit_of_meaning/<int:unit_of_meaning_id>/<str:language_code>/', list_translations_in_language_for_unit_of_meaning, name='list_translations_in_language_for_unit_of_meaning'),
    path('get_unit_of_meaning/<int:unit_of_meaning_id>/', get_unit_of_meaning, name='get_unit_of_meaning'),
]