from django.urls import path
from .views import *

app_name = 'calendario'
urlpatterns = [
    path('listado_calendario/', Calendario_View.as_view(), name = 'listado_calendario'),
    
    path('crear_calendario/', Calendario_Create.as_view(), name = 'crear_calendario'),

    path('editar_planificacion/<int:pk>', Calendario_Update.as_view(), name = 'editar_calendario'),
    
    path('listar_planificacion/', CalendarioUsuario_View.as_view(), name = 'listar_planificacion'),

    path('InactivarActivarCalendario/<int:pk>', InactivarActivarCalendario.as_view(), name = 'InactivarActivarCalendario'),
    
    path('crear_planificacion/', CalendarioUsuario_Create.as_view(), name = 'crear_planificacion'),

    path('InactivarActivarPlanificacion/<int:pk>', InactivarActivarPlanificacion.as_view(), name = 'InactivarActivarPlanificacion'),

]