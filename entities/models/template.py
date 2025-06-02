from django.db import models
from django.contrib.auth.models import User

class Template(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    

class TemplateField(models.Model):
    key = models.CharField(max_length=255)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.key + ":" + self.value

    class Meta:
        unique_together = ('key', 'template')
        abstract = True

class TemplateFieldTranslation(TemplateField):
    value = models.TextField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = "translation"

class TemplateFieldTargetLanguage(TemplateField):
    value = models.TextField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = "target_language"

class TemplateFieldLink(TemplateField):
    value = models.URLField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = "link"

class TemplateFieldImage(TemplateField):
    value = models.ImageField(upload_to='templates/images/')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = "image"

