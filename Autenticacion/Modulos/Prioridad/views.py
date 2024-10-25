from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from Modulos.Prioridad.models import Prioridad
from Modulos.Prioridad.forms import PrioridadForms
# Create your views here.

class CreatePrioridad(LoginRequiredMixin, CreateView):
    model = Prioridad
    template_name = 'Inicio.html'
    form_class = PrioridadForms

