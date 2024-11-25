from django.apps import AppConfig


class ReportesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Modulos.Agente.Reportes'

    def ready(self):
        # Importa el módulo de señales
        import Modulos.Agente.Reportes.signals
        