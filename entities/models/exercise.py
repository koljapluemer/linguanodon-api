from django.contrib.postgres.fields import ArrayField
from django.db import models
from entities.models.learning_goal import LearningGoal
class Exercise(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instructions = models.TextField()
    extra_info_before_solve = models.TextField()
    extra_info_after_solve = models.TextField()
    learning_goals = models.ManyToManyField(LearningGoal)

    class Meta:
        abstract = True


class ExerciseClozeChooseFromHardCodedTwo(Exercise):
    cloze = models.TextField()
    replace_start_index = models.IntegerField()
    replace_end_index = models.IntegerField()
    correct_choice = models.TextField()
    incorrect_choice = models.TextField()

    @property
    def clozed_content(self):
        return self.cloze[:self.replace_start_index] + "_" * (self.replace_end_index - self.replace_start_index) + self.cloze[self.replace_end_index:]

    def __str__(self):
        return self.clozed_content

