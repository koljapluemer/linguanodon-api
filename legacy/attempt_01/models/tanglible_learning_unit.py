from django.db import models

from linguanodon.models.learning_unit import LearningUnit

# note: derives from LearningUnit!
class TanglibleLearningUnit(LearningUnit):
    text = models.TextField()
    pronunciation = models.TextField(blank=True, null=True)
    type_info = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    translations = models.ManyToManyField('self', blank=True)
    synonyms = models.ManyToManyField('self', blank=True)
    similar_but_not_synonyms = models.ManyToManyField('self', blank=True)

    license = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    owner_link = models.URLField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-updated_at', 'text']
        unique_together = ('text', 'type_info')

    def __str__(self):
        return self.text
