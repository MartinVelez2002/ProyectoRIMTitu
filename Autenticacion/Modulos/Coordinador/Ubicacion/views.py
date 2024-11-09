from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.conf import settings

from Modulos.Coordinador.Ubicacion.models import Ubicacion_Model
from Modulos.Coordinador.Ubicacion.forms import Ubicacion_Form


class Ubicacion_View(LoginRequiredMixin, ListView):
    model = Ubicacion_Model
    template_name = 'ubicacion.html'
    context_object_name = 'ubicacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('ubicacion:crear_ubicacion')
        context['title_table'] = 'Listado de Ubicaciones'
        return context

class Ubicacion_Create(LoginRequiredMixin, CreateView):
    model = Ubicacion_Model
    template_name = 'registrar_ubicacion.html'
    form_class = Ubicacion_Form
    success_url = revese_lazy('ubicacion:inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Ubicación'
        context['cancelar'] = reverse('ubicacion:inicio')
        context['action_save'] = self.request.path
        context['google_maps_api_key'] = settings.GOOGLE_API_KEY
        return context
    
    
    
# Create your views here.
