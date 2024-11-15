from django.apps import AppConfig


class ReportesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Modulos.Agente.Reportes'

    def ready(self):
        import Modulos.Agente.Reportes.signals  # Importa las señales al iniciar la aplicación