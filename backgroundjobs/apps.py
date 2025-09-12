from django.apps import AppConfig


class BackgroundjobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backgroundjobs'
    def ready(self):
        import backgroundjobs.task

    
   