from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from Modulos.Prioridad.views import CreatePrioridad

app_name = 'Prioridad'
urlpatterns = [
    path('', CreatePrioridad.as_view(), name='prioridad'),
]