from django.shortcuts import redirect
from django.db.models import Case, When, Value, IntegerField
from Modulos.Agente.Reportes.models import CabIncidente_Model, DetIncidente_Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages
from Modulos.Coordinador.Ubicacion.models import *

# Create your views here.

class ListarReportes_View(LoginRequiredMixin, ListView):
    model = CabIncidente_Model
    template_name = 'listado_reportes_agente.html'
    paginate_by = 5
    context_object_name = 'rep'
    
    def get_queryset(self):
        # Obtener los valores de los filtros
        ubicacion_query = self.request.GET.get('query')  # Filtro por ubicación

        # Asignar valores numéricos a cada prioridad para el orden personalizado
        queryset = CabIncidente_Model.objects.annotate(
            prioridad_orden=Case(
                When(prioridad='A', then=Value(1)),  # Alto tiene mayor prioridad
                When(prioridad='M', then=Value(2)),  # Medio
                When(prioridad='B', then=Value(3)),  # Bajo
                default=Value(4),
                output_field=IntegerField(),
            )
        ).prefetch_related('detalles').order_by('prioridad_orden', '-fecha', '-id')  # Ordenar por prioridad, fecha y ID
        
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

    def post(self, request, *args, **kwargs):
        incidente_id = request.POST.get('incidente_id')  # Obtener el ID del incidente (de un campo oculto o similar)
        try:
            incidente = CabIncidente_Model.objects.get(id=incidente_id)  # Obtener el incidente
        except CabIncidente_Model.DoesNotExist:
            messages.error(request, "El incidente especificado no existe.")
            return redirect('reportesCoord:listado_reportes_agente')  # Redirigir si no se encuentra el incidente
        
       
        
        incidente = CabIncidente_Model.objects.get(id=incidente_id)  # Obtener el incidente
        nuevo_estado = request.POST.get("nuevo_estado")
        descripcion = request.POST.get("descripcion")
        evidencia = request.FILES.get("evidencia")
        comentarios = request.POST.get("comentarios")# Obtener archivo de evidencia (si se carga)


        # Validar que el estado ya no exista en los detalles del incidente
        if incidente.detalles.filter(estado_incidente=nuevo_estado).exists():
            messages.error(request, "No es posible cambiar el estado del incidente a un estado pasado.")
            return redirect('reportesCoord:listado_reportes_agente')
        
        
        # Verifica si se cambió el estado y si hay una nueva descripción
        if nuevo_estado:
            # Crear un nuevo detalle con el cambio de estado y la posible evidencia
            DetIncidente_Model.objects.create(
                cabincidente=incidente,
                estado_incidente=nuevo_estado,
                descripcion=descripcion,  # Descripción sobre el estado del incidente
                evidencia=evidencia,  # Si se adjuntó una evidencia, se guarda
                comentarios_adicionales= comentarios 
            )
        

            # Actualizar el estado del incidente
            incidente.estado_incidente = nuevo_estado
            incidente.save()
            
            messages.success(request, "Estado del incidente actualizado correctamente.")
        else:
            messages.error(request, "Debe seleccionar un nuevo estado para el incidente.")

        return redirect('reportesCoord:listado_reportes_agente')  # Asegúrate de que la URL esté correcta