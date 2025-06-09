from django.db import models

class LearningUnit(models.Model):
    language_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    parents = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="children")

    updated_at = models.DateTimeField(auto_now=True)
    creation_context = models.TextField(default="Unknown")

    class Meta:
        ordering = ['-updated_at', 'name']
        unique_together = ('language_code', 'name')
    def __str__(self):
        return self.name

