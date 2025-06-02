from django.db import models

from entities.models.topic import Topic

class LearningGoal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.name

