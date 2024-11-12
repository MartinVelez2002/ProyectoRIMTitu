from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from Modulos.Coordinador.Calendario.models import *
from Modulos.Coordinador.Calendario.forms import *
from django.contrib import messages
# Create your views here.

class Calendario_View(LoginRequiredMixin, ListView):
    model = Calendario_Model
    template_name = 'listado_calendario.html'
    context_object_name = 'calendario'
    paginate_by = 5
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('calendario:crear_calendario')
        context['title_table'] = 'Listado del Calendario'
        
        return context
    

    
class Calendario_Create(LoginRequiredMixin, CreateView):
    model = Calendario_Model
    template_name = 'crear_calendario.html'
    success_url = reverse_lazy('calendario:listado_calendario')
    form_class = Calendario_Form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Calendario'
        context['cancelar'] = reverse('calendario:listado_calendario')
        context['action_save'] = self.request.path
        return context


class CalendarioUsuario_View(LoginRequiredMixin, ListView):
    model = TurnUsuario_Model
    template_name = 'listado_planificacion.html'
    context_object_name = 'calendarioUs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('calendario:crear_planificacion')
        context['title_table'] = 'Listado de Planificación'
        
        return context

class CalendarioUsuario_Create(LoginRequiredMixin, CreateView):
    model = Turno_Model
    template_name = 'crear_planificacion.html'
    form_class = TurnUsuarioUbicacion_Form
    success_url = reverse_lazy('calendario:listar_planificacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Planificación'
        context['cancelar'] = reverse('calendario:listar_planificacion')
        context['action_save'] = self.request.path
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar solo usuarios válidos para el select
        form.fields['Usuario'].queryset = Usuario.objects.filter(is_superuser=False)
        return form