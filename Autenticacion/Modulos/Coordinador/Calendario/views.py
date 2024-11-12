from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from Modulos.Coordinador.Calendario.models import *
from Modulos.Coordinador.Calendario.forms import *
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
    def form_valid():
        calendario = form.save(commit= False)
        calendario.Estado = True
        calendario.save()
        return super().form_valid(form)
    
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
