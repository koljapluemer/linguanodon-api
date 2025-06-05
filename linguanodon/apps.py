from django.apps import AppConfig


class LinguanodonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'linguanodon'
    
    def ready(self):
        import linguanodon.models
