from django.db import models

from entities.models.learning_goal import LearningGoal

class UnitOfMeaning(models.Model):
    based_on_meaning = models.TextField(unique=True)
    image = models.ImageField(upload_to='unit_of_meaning_images/', blank=True, null=True)
    learning_goals = models.ManyToManyField(LearningGoal, blank=True)

    def __str__(self):
        return self.based_on_meaning
