from django.urls import path
from .views import *

app_name = 'reportes'
urlpatterns =[
    path('listar_reportes/', Reportes_View.as_view(), name = 'listar_reportes'),

    path('crear_reporte/', Reportes_Create.as_view(), name = 'crear_reporte'),
]