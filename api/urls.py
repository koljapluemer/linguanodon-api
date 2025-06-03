from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.enpoints.learning_goals.list_learning_goals import LearningGoalViewSet
from api.enpoints.units_of_meaning.list_units_of_meaning_per_language_goal import UnitOfMeaningViewSet

router = DefaultRouter()
router.register(r'learning-goals', LearningGoalViewSet, basename='learning-goal')
router.register(r'units-of-meaning', UnitOfMeaningViewSet, basename='unit-of-meaning')
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
