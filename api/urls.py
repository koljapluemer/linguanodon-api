from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.enpoints.learning_goals.list_learning_goals import LearningGoalViewSet

router = DefaultRouter()
router.register(r'learning-goals', LearningGoalViewSet, basename='learning-goal')

urlpatterns = [
    path('', include(router.urls)),
]
