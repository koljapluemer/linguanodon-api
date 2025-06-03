from django.db import models

from entities.models.language import Language
from entities.models.unit_of_meaning import UnitOfMeaning


class Translation(models.Model):
    text = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    unit_of_meaning = models.ForeignKey(UnitOfMeaning, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    creation_context = models.TextField(default="Unknown")
    license = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    owner_link = models.URLField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.text
