from django.db import models
from django.contrib.auth.models import User
from entities.models.language import Language
class LearningGoal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parents = models.ManyToManyField("self", blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    derived_from = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name

