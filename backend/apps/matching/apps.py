from django.apps import AppConfig


class MatchingConfig(AppConfig):
    name = "apps.matching"
    verbose_name = "Sophisticated matching app"

    def ready(self):
        from . import checks  # noqa: F401
