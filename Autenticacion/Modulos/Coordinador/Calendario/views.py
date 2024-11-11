from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from Modulos.Coordinador.Calendario.models import *
from Modulos.Coordinador.Calendario.forms import *
# Create your views here.

class Calendario_View(ListView):
    template_name = 'listado_calendario.html'
    model = Calendario_Model
    paginate_by = 5
    context_object_name = 'calendario'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('calendario:listar_calendario')
        context['title_table'] = 'Listado de Calendario'

        return context
    
class Calendario_Create(CreateView):
    model = Calendario_Model
    template_name = 'crear_calendario.html'
    form_class = Calendario_Form
    success_url = reverse('calendario:crear_calendario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Calendario'
        context['cancelar'] = reverse('calendario:crear_calendario')
        context['action_save'] = self.request.path

        return context
    
    def form_valid(self, form):
        calendario = form.save(commit= False)
        calendario.Estado = True
        calendario.save()
        return super().form_valid(form)