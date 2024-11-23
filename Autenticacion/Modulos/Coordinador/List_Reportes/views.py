from django.shortcuts import render
from Modulos.Agente.Reportes.models import CabIncidente_Model, DetIncidente_Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from Modulos.Coordinador.Ubicacion.models import *
from Auth.constantes import Opciones
# Create your views here.

class ListarReportes_View(LoginRequiredMixin, ListView):
    model = CabIncidente_Model
    template_name = 'listado_reportes_agente.html'
    paginate_by = 5
    context_object_name = 'rep'
    
    def get_queryset(self):
        # Obtener los valores de los filtros
        ubicacion_query = self.request.GET.get('query')  # Filtro por ubicación
    
        # Construir el queryset base con relaciones prefetechadas
        queryset = CabIncidente_Model.objects.prefetch_related('detalles')

        # Aplicar los filtros si están definidos
        if ubicacion_query:
            queryset = queryset.filter(agente__ubicacion__id=ubicacion_query)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Reportes de los Agentes'
        context['ubicaciones'] = Ubicacion_Model.objects.all()
        context['query'] = self.request.GET.get('query', '')  # Retener el valor seleccionado
        return context
