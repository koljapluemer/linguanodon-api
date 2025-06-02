from django.db import models
from django.contrib.auth.models import User
from entities.models.language import Language
from entities.models.learning_goal import LearningGoal
class Template(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    learning_goals = models.ManyToManyField(LearningGoal)

    derived_from = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    field_translation = models.TextField(blank=True, null=True)
    field_target_language = models.TextField(blank=True, null=True)
    field_link = models.URLField(blank=True, null=True)
    field_image = models.ImageField(blank=True, null=True)

