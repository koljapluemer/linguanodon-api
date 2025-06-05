from django.db import models

class UnitOfMeaning(models.Model):
    text = models.TextField()
    language_code = models.CharField(max_length=255)
    pronunciation = models.TextField(blank=True, null=True)
    type_info = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # implies also synonyms in the same language (for now, not sure about sensibility)
    translations = models.ManyToManyField('self', blank=True)
    synonyms = models.ManyToManyField('self', blank=True)
    similar_but_not_synonyms = models.ManyToManyField('self', blank=True)

    learning_goals = models.ManyToManyField('entities.LearningGoal', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    creation_context = models.TextField(default="Unknown")
    license = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    owner_link = models.URLField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-updated_at', 'text']
        unique_together = ('text', 'language_code', 'type_info')

    def __str__(self):
        return self.text
