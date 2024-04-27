from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        from django.db.models.signals import post_save
        from . import signals, models

        post_save.connect(signals.account_post_save, sender=models.Account)