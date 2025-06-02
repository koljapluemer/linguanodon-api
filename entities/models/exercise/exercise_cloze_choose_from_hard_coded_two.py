from django.db import models
from entities.models.exercise.exercise import Exercise


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

