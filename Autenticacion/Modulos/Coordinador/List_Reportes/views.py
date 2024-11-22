from django.shortcuts import render
from Modulos.Agente.Reportes.models import CabIncidente_Model, DetIncidente_Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

# Create your views here.

class ListarReportes_View(LoginRequiredMixin, ListView):
    model = CabIncidente_Model
    template_name = 'listado_reportes_agente.html'
    paginate_by = 5
    context_object_name = 'rep'
    
    def get_queryset(self):
        # Usamos prefetch_related para traer detalles relacionados en una sola consulta
        return CabIncidente_Model.objects.prefetch_related('detalles')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Reportes de los Agentes'
        
        return context
