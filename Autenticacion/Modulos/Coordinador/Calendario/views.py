from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from Modulos.Coordinador.Calendario.models import *
from Modulos.Coordinador.Calendario.forms import *

from Modulos.Login.mixin import CambiarEstadoMixin, RoleRequiredMixin

# Create your views here.

class Calendario_View(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Calendario_Model
    required_role = 'Coordinador'
    template_name = 'listado_calendario.html'
    context_object_name = 'calendario'
    paginate_by = 5
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('calendario:crear_calendario')
        context['title_table'] = 'Listado del Calendario'
        
        return context

class Calendario_Create(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Calendario_Model
    required_role = 'Coordinador'
    template_name = 'crear_calendario.html'
    success_url = reverse_lazy('calendario:listado_calendario')
    form_class = Calendario_Form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Calendario'
        context['cancelar'] = reverse('calendario:listado_calendario')
        context['action_save'] = self.request.path
        
        return context

class Calendario_Update(LoginRequiredMixin, RoleRequiredMixin, UpdateView ):
    model = Calendario_Model
    required_role = 'Coordinador'
    template_name = 'crear_calendario.html'
    success_url = reverse_lazy('calendario:listado_calendario')
    form_class = Calendario_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edición de Calendario'
        context['cancelar'] = reverse('calendario:listado_calendario')
        context['action_save'] = self.request.path
        return context

class InactivarActivarCalendario(CambiarEstadoMixin, RoleRequiredMixin):
    model = Calendario_Model
    required_role = 'Coordinador'
    redirect_url = 'calendario:listado_calendario'





class CalendarioUsuario_View(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = TurnUsuario_Model
    required_role = 'Coordinador'
    template_name = 'listado_planificacion.html'
    context_object_name = 'calendarioUs'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('calendario:crear_planificacion')
        context['title_table'] = 'Listado de Planificación'
        context['dir_search'] = self.request.path  # Para mantener el buscador en la misma URL
        context['query'] = self.request.GET.get('query', '')  # Capturar el filtro actual
        # Obtener todos los lugares disponibles
        context['lugares'] = Ubicacion_Model.objects.all()  # Cambia `Lugar_Model` al modelo real que contiene los lugares
        return context

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        if query:
            return self.model.objects.filter(
                ubicacion__lugar__icontains=query  # Filtra por el campo `lugar` en el modelo relacionado `Ubicacion_Model`
            )
        return self.model.objects.all()



class CalendarioUsuario_Create(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = TurnUsuario_Model
    required_role = 'Coordinador'
    template_name = 'crear_planificacion.html'
    success_url = reverse_lazy('calendario:listar_planificacion')
    form_class = TurnUsuarioUbicacion_Form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Planificación'
        context['cancelar'] = reverse('calendario:listar_planificacion')
        context['action_save'] = self.request.path
        
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar solo usuarios válidos para el select
        form.fields['usuario'].queryset = Usuario.objects.filter(rol__id=1)
        form.fields['calendario'].queryset = Calendario_Model.objects.filter(estado=True)
        form.fields['turno'].queryset = Turno_Model.objects.filter(estado=True)
        form.fields['ubicacion'].queryset = Ubicacion_Model.objects.filter(estado=True)
        return form
    

class InactivarActivarPlanificacion(CambiarEstadoMixin):
    model = TurnUsuario_Model
    redirect_url = 'calendario:listar_planificacion'