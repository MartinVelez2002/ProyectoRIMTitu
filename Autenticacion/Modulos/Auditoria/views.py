from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from Modulos.Login.views import RoleRequiredMixin
from .models import AuditoriaUser


class Auditoria_View(LoginRequiredMixin, RoleRequiredMixin, ListView ):
    template_name = 'listar_auditoria.html'
    context_object_name = 'auditoria'
    model = AuditoriaUser
    required_role = 'Coordinador'
    paginate_by = 5
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dir_search'] = self.request.path
        context['query'] = self.request.GET.get('query', '')
        context['title_table'] = 'Tabla de Auditoría'
        return context
    

