from .views import ListarReportes_View
from django.urls import path

app_name = 'reportesCoord'
urlpatterns = [
    path('listado_reportes_agente/', ListarReportes_View.as_view(), name = 'listado_reportes_agente'),
]
