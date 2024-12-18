from django.apps import AppConfig


class KeepSessionData(AppConfig):
    name = "core"

    def ready(self):
        # Importa o módulo de sinais para registrar os sinais
        import core.signals
