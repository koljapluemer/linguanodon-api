from django.contrib.postgres.fields import ArrayField
from django.db import models
from entities.models.learning_goal import LearningGoal

from django.contrib.auth.models import User

class Exercise(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instructions = models.TextField()
    extra_content_before_solve = models.TextField()
    extra_content_after_solve = models.TextField()
    learning_goals = models.ManyToManyField(LearningGoal)
    is_public = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    derived_from = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        abstract = True


