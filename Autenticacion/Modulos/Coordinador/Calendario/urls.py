from django.urls import path
from .views import *

app_name = 'calendario'

urlspatterns = [
    path('listar_calendario/', Calendario_View.as_view(), name = 'listar_calendario'),

    path('crear_calendario/', Calendario_Create.as_view(), name = 'crear_calendario'),


    
]