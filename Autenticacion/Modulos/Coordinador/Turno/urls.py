from django.urls import path
from .views import Turn_View, Turn_Create
app_name = 'turno'
urlpatterns=[
    path('listar_turno/', Turn_View.as_view(), name = 'listar_turno'),

    path('crear_turno/', Turn_Create.as_view(), name = 'crear_turno'),

]