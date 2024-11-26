from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.db.models import Case, When, Value, IntegerField, Count, Subquery, OuterRef, Q
from Modulos.Agente.Reportes.models import CabIncidente_Model, DetIncidente_Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from Modulos.Coordinador.Ubicacion.models import *
from Modulos.Login.mixin import RoleRequiredMixin
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

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
    
    
from django.db.models import Count, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce




class DashboardView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'dashboards.html'
    required_role = 'Coordinador'
    model = CabIncidente_Model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Subquery para obtener el estado más reciente de cada incidente
        subquery_estado = DetIncidente_Model.objects.filter(
            cabincidente=OuterRef('id')
        ).order_by('-hora').values('estado_incidente')[:1]

        # Anotar el estado más reciente en cada CabIncidente_Model
        incidentes_con_estado = CabIncidente_Model.objects.annotate(
            estado_reciente=Coalesce(Subquery(subquery_estado), Value('N'))  # Default 'N' si no hay estado
        )

        # Gráficos por estado más reciente
        reportes_por_estado = (
            incidentes_con_estado
            .values('estado_reciente')
            .annotate(cantidad=Count('estado_reciente'))
            .order_by('estado_reciente')
        )

        # Gráficos por prioridad
        reportes_por_prioridad = (
            CabIncidente_Model.objects
            .values('prioridad')
            .annotate(cantidad=Count('prioridad'))
            .order_by('prioridad')
        )

        # Preparar los datos para la plantilla
        context['reportes_por_estado'] = list(reportes_por_estado)
        context['reportes_por_prioridad'] = list(reportes_por_prioridad)
        return context


# GENERACIÓN DE PDF
def generar_reporte_incidente(request, incidente_id):
    # Recuperar el incidente con su detalle
    try:
        cabecera = CabIncidente_Model.objects.get(id=incidente_id)
        detalles = cabecera.detalles.all()  # Relación definida por related_name='detalles'

        # Preparar contexto
        context = {
            "cabecera": cabecera,
            "detalles": detalles,
        }

        # Cargar la plantilla HTML
        template = get_template("reporte_incidente.html")
        html = template.render(context)

        # Generar el PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="reporte_incidente_{incidente_id}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error al generar el PDF", content_type="text/plain")
        return response
    except CabIncidente_Model.DoesNotExist:
        return HttpResponse("Incidente no encontrado", content_type="text/plain")
