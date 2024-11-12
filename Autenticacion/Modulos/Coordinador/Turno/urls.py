from django.urls import path
from .views import *



app_name = 'turno'
urlpatterns=[
    path('listar_turno/', Turn_View.as_view(), name = 'listar_turno'),

    path('crear_turno/', Turn_Create.as_view(), name = 'crear_turno'),

    path('inactivar_turno/<int:pk>/', InactivarActivarTurnoView.as_view(), name='inactivar_activar_turno')
    

]