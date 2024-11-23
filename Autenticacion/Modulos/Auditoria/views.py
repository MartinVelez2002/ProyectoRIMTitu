from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from Modulos.Auditoria.models import AuditoriaUser  # Modelo principal
from Modulos.Auditoria.models import AuditoriaUser  # Subclase para acciones
from Modulos.Login.mixin import RoleRequiredMixin


class Auditoria_View(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'listar_auditoria.html'
    context_object_name = 'auditoria'
    model = AuditoriaUser
    required_role = 'Coordinador'
    paginate_by = 3

    def get_queryset(self):
        """
        Puedes extender el filtrado aquí si necesitas buscar auditorías 
        por acciones específicas o por otros criterios basados en query params.
        """
        query = self.request.GET.get('query')
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(
                descripcion__icontains=query
            )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Agrega al contexto la lista de acciones disponibles (AccionChoices)
        para mostrarlas en el filtro del template o cualquier otra lógica.
        """
        context = super().get_context_data(**kwargs)
        context['dir_search'] = self.request.path
        context['query'] = self.request.GET.get('query', '')
        context['title_table'] = 'Tabla de Auditoría'
        context['acciones'] = AuditoriaUser.AccionChoices.choices  # Lista de acciones disponibles
        return context
