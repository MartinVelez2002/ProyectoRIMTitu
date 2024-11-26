from django.shortcuts import redirect
from datetime import datetime
from django.db.models.functions import TruncDay
from django.db.models import Case, When, Value, IntegerField, Count, Subquery, OuterRef
from Modulos.Agente.Reportes.models import CabIncidente_Model, DetIncidente_Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from Modulos.Coordinador.Ubicacion.models import *
from Modulos.Login.mixin import RoleRequiredMixin


# Create your views here.

class ListarReportes_View(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = CabIncidente_Model
    required_role = 'Coordinador'
    template_name = 'listado_reportes_agente.html'
    paginate_by = 5
    context_object_name = 'rep'
    
    
    def get_queryset(self):
          
        # Obtener los valores de los filtros
        ubicacion_query = self.request.GET.get('query')  # Filtro por ubicación
        prioridad_query = self.request.GET.get('prioridad')  # Filtro por prioridad
        estado_query = self.request.GET.get('estado')
       
         # Anotar el estado más reciente de cada incidente
        subquery_estado = DetIncidente_Model.objects.filter(
            cabincidente=OuterRef('id')
        ).order_by('-hora').values('estado_incidente')[:1]  # Obtener el estado más reciente

        
        queryset = CabIncidente_Model.objects.annotate(
            estado_actual=Subquery(subquery_estado)
        ).annotate(
            prioridad_orden=Case(
                When(prioridad='A', then=Value(1)),  # Alto tiene mayor prioridad
                When(prioridad='M', then=Value(2)),  # Medio
                When(prioridad='B', then=Value(3)),  # Bajo
                default=Value(4),
                output_field=IntegerField(),
            )
        ).prefetch_related('detalles').order_by('prioridad_orden', '-fecha', 'id')  # Orden personalizado
        
        
    
        
        # Aplicar los filtros si están definidos
        if ubicacion_query:
            queryset = queryset.filter(agente__ubicacion__id=ubicacion_query)

        if prioridad_query:
            queryset = queryset.filter(prioridad=prioridad_query)
        
        if estado_query:
            # Filtrar por el estado más reciente anotado
            queryset = queryset.filter(estado_actual=estado_query)
        


        return queryset 
    

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        # Obtener el último detalle para cada cabecera de incidente
        ultimo_detalle = DetIncidente_Model.objects.filter(
            cabincidente=OuterRef('id')
        ).order_by('-hora')

        # Consultar las cabeceras con el estado del último detalle
        estados = CabIncidente_Model.objects.annotate(
            estado_actual=Subquery(ultimo_detalle.values('estado_incidente')[:1])
        ).values('estado_actual').annotate(total=Count('id'))

        # Convertir los resultados en un diccionario
        estados_dict = {item['estado_actual']: item['total'] for item in estados}

        # Crear el resumen
        resumen_estados = {
            'pendientes': estados_dict.get('N', 0),  # Notificados
            'en_proceso': estados_dict.get('E', 0), # En proceso
            'atendidos': estados_dict.get('A', 0),  # Atendidos
            'cerrados': estados_dict.get('C', 0) #Cerrados
        }

        context['resumen_estados'] = resumen_estados
        context['title_table'] = 'Reportes de los Agentes'
        context['ubicaciones'] = Ubicacion_Model.objects.all()
        context['query'] = self.request.GET.get('query', '')  # Retener el valor seleccionado
        context['action_save'] = self.request.path
        context['prioridad'] = self.request.GET.get('prioridad', '')
        context['estado'] = self.request.GET.get('estado', '')
     
       

        
        
        
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
    
 
 




class DashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'dashboards.html'
    required_role = 'Coordinador'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos de prioridades
        prioridades = CabIncidente_Model.objects.values('prioridad').annotate(count=Count('id'))
        labels = ['Alto', 'Bajo', 'Medio']
        data = [p['count'] for p in prioridades]
        
  
        # Datos de incidencias por agente
        incidencias_por_agente = CabIncidente_Model.objects.values('agente__usuario__nombre').annotate(count=Count('id')).order_by('-count')
        agentes = [item['agente__usuario__nombre'] for item in incidencias_por_agente]
        incidencias = [item['count'] for item in incidencias_por_agente]

      
        # Resumen general de incidencias
        total_incidencias = CabIncidente_Model.objects.count()
        
       

         # Obtener incidencias agrupadas por ubicación
        incidencias_por_ubicacion = CabIncidente_Model.objects.values('agente__ubicacion__lugar').annotate(count=Count('id')).order_by('agente__ubicacion__lugar')
        
        # Extraer etiquetas (ubicaciones) y datos (conteo de incidencias)
        ubicaciones = [incidencia['agente__ubicacion__lugar'] for incidencia in incidencias_por_ubicacion]
        incidencias_por_ubicacion_data = [incidencia['count'] for incidencia in incidencias_por_ubicacion]
        
        # Agregar los datos al contexto
        context['ubicaciones'] = ubicaciones
        context['incidencias_por_ubicacion'] = incidencias_por_ubicacion_data
       
     
        context['total_incidencias'] = total_incidencias
      
        
        context['labels'] = labels
        context['data'] = data
        
        # Agregar datos de incidencias por agente
        context['agentes'] = agentes
        context['incidencias'] = incidencias
        
        return context