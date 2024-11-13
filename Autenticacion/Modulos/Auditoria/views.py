from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AuditoriaUser


class Auditoria_View(LoginRequiredMixin, ListView):
    template_name = 'listar_auditoria.html'
    context_object_name = 'auditoria'
    model = AuditoriaUser
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dir_search'] = self.request.path
        context['query'] = self.request.GET.get('query', '')
        context['title_table'] = 'Tabla de Auditoría'
        return context
    

# Create your views here.
