from django.db import models
from django.contrib.auth.models import User
from entities.models.language import Language
class LearningGoal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    parents = models.ManyToManyField("self", blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name

