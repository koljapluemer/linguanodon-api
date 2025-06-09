from django.db import models

class Translation(models.Model):

    pronunciation = models.CharField(max_length=255, blank=True, null=True)
    type_info = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    license = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    owner_link = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)

    creation_context = models.CharField(max_length=255, default="Manual by User")