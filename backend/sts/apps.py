from django.apps import AppConfig


class StsConfig(AppConfig):
    name = "sts"

    def ready(self):
        from . import signals  # noqa: F401
