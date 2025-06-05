from django.db import models

from entities.models.learning_goal import LearningGoal

class UnitOfMeaning(models.Model):
    text = models.TextField()
    language_code = models.CharField(max_length=255)
    pronunciation = models.TextField(blank=True, null=True)

    translations = models.ManyToManyField('self', blank=True)

    learning_goals = models.ManyToManyField(LearningGoal, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    creation_context = models.TextField(default="Unknown")
    license = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    owner_link = models.URLField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-updated_at', 'text']

    def __str__(self):
        return self.text
