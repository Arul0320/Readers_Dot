from django.apps import AppConfig

class RDConfig(AppConfig):  # Note the all-caps RD to match what Django expects
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'