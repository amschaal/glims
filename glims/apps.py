from django.apps import AppConfig

class GlimsConfig(AppConfig):
    name = 'glims'
    verbose_name = "GLIMS"
    def ready(self):
        import notification_signals