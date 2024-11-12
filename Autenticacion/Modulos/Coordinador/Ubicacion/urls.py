from django.urls import path
from .views import *

app_name = 'ubicacion'

urlpatterns=[
    path('inicio/', Ubicacion_View.as_view(), name = 'inicio'),

    path('crear_ubicacion/', Ubicacion_Create.as_view(), name = 'crear_ubicacion'),
    
    path('inactivar_ubicacion/<int:pk>/', InactivarActivarUbicacionView.as_view(), name='inactivar_activar_ubicacion')
]