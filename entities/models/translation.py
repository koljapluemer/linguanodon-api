from django.db import models

from entities.models.language import Language
from entities.models.unit_of_meaning import UnitOfMeaning


class Translation(models.Model):
    text = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    unit_of_meaning = models.ForeignKey(UnitOfMeaning, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
