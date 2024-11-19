from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

# Create your views here.
class Reportes_View(LoginRequiredMixin, ListView):

    template_name = 'listar_reportes.html'
    paginate_by = 5
    context_object_name = 'rep'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('reportes:crear_reporte')
        context['title_table'] = 'Listado de mis Reportes'
        return context

class Reportes_Create(LoginRequiredMixin, CreateView):
    template_name = 'crear_reportes.html'
    success_url = reverse_lazy('reportes:listar_reportes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario de Reportes'
        context['cancelar'] = reverse('reportes:listar_reportes')
        context['action_save'] = self.request.path
        
        return context
