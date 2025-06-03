from rest_framework import serializers
from entities.models.learning_goal import LearningGoal

class LearningGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningGoal
        fields = ['id', 'name'] 