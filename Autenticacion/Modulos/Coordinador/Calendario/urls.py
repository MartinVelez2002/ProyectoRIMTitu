from django.urls import path
from .views import *

app_name = 'calendario'
urlpatterns = [
    path('listado_calendario/', Calendario_View.as_view(), name = 'listado_calendario'),
    
    path('crear_calendario/', Calendario_Create.as_view(), name = 'crear_calendario'),
]