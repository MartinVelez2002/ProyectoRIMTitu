from .views import *
from django.urls import path

app_name = 'reportesCoord'
urlpatterns = [
    path('listado_reportes_agente/', ListarReportes_View.as_view(), name = 'listado_reportes_agente'),
    path('resumen_datos/', DashboardView.as_view(), name = 'resumen_datos'),
    path('reporte/<int:incidente_id>/', generar_reporte_incidente, name='reporte_incidente'),

]
