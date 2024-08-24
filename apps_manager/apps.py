from django.apps import AppConfig


class AppsManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps_manager'
    def ready(self):
        import apps_manager.signals
