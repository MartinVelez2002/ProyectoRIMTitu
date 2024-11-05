from django.shortcuts import render
from Modulos.Coordinador.Novedad.models import TipoNovedad_Model, Novedad_Model
from Modulos.Coordinador.Novedad.forms import Novedad_form, TipoNovedad_form
from django.views.generic import TemplateView, CreateView, ListView
from django.urls import reverse_lazy, reverse

class Novedad_View(ListView):
    template_name = 'novedad.html'
    context_object_name = 'novedad'
    model = Novedad_Model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('novedad:crear_novedad')
        context['title_table'] = 'Listado de Novedades'

        return context

class Novedad_Create(CreateView):
    model = Novedad_Model
    template_name = 'registrar_novedad.html'
    form_class = Novedad_form
    success_url = reverse_lazy('novedad:inicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Novedad'
        context['cancelar'] = reverse('novedad:inicio')
        context['action_save'] = self.request.path
        
        return context

class TipoNovedad_View(ListView):
    template_name = 'tipNov.html'
    model = TipoNovedad_Model
    context_object_name = 'tipNov'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('novedad:crear_tipNov')
        context['title_table'] = 'Listado Tipo de Novedades'

        return context
    
class TipoNovedad_Create(CreateView):
    model = TipoNovedad_Model
    template_name = 'registrar_tipNovedad.html'
    form_class = TipoNovedad_form
    success_url = reverse_lazy('novedad:inicio_tipoNov')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Tipo de Novedad'
        context['cancelar'] = reverse('novedad:inicio_tipoNov')
        context['action_save'] = self.request.path
        
        return context