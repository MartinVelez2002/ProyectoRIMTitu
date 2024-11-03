from django.shortcuts import render
from Modulos.Coordinador.Novedad.models import TipoNovedad_Model, Novedad_Model
from django.views.generic import TemplateView, CreateView

class Novedad_View(TemplateView):
    template_name = 'novedad.html'


# Create your views here.
