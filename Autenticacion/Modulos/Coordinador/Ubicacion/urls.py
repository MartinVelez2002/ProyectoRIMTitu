from django.urls import path
from .views import Ubicacion_View, Ubicacion_Create

app_name = 'ubicacion'

urlpatterns = [
    path('inicio/', Ubicacion_View.as_view(), name = 'inicio'),

    path('crear_ubicacion/', Ubicacion_Create.as_view(), name = 'crear_ubicacion')
    
    
]