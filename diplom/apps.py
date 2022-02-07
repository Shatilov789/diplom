from django.apps import AppConfig


class BackendConfig(AppConfig):

    name = 'diplom'

    def ready(self):
        "импортируемы сигналы"
