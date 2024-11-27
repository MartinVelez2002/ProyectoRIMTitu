from django.shortcuts import redirect
from django.db.models.functions import TruncMonth
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
            cabincidente=OuterRef('pk')
        ).order_by('-hora')

        # Consultar las cabeceras con el estado del último detalle
        estados = CabIncidente_Model.objects.annotate(
            estado_actual=Subquery(ultimo_detalle.values('estado_incidente')[:1])
        ).values('estado_actual').annotate(total=Count('id'))

        # Convertir los resultados en un diccionario
        estados_dict = {item['estado_actual']: item['total'] for item in estados}

        # Crear el resumen de estados
        resumen_estados = {
            'pendientes': estados_dict.get('N', 0),  # Notificados
            'en_proceso': estados_dict.get('E', 0), # En proceso
            'atendidos': estados_dict.get('A', 0),  # Atendidos
            'cerrados': estados_dict.get('C', 0)    # Cerrados
        }

        # Agregar el resumen a tu contexto
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
        # Accede al request a través de self.request
        request = self.request
        
        context = super().get_context_data(**kwargs)
        
        # Obtener el mes seleccionado o 'todos' si no se ha seleccionado ninguno
        mes_param = request.GET.get('mes', 'todos')
        
        # Filtrar incidentes por el mes seleccionado
        if mes_param != 'todos':
            year = int(mes_param[:4])
            month = int(mes_param[5:7])
            fecha_filter = {'fecha__year': year, 'fecha__month': month}
        else:
            fecha_filter = {}

        # Datos de prioridades
        prioridades = CabIncidente_Model.objects.filter(**fecha_filter).values('prioridad').annotate(count=Count('id'))
        labels = ['Alto', 'Bajo', 'Medio']
        data = [p['count'] for p in prioridades]
        
        # Datos de incidencias por agente
        incidencias_por_agente = CabIncidente_Model.objects.filter(**fecha_filter).values('agente__usuario__nombre').annotate(count=Count('id')).order_by('-count')
        agentes = [item['agente__usuario__nombre'] for item in incidencias_por_agente]
        incidencias = [item['count'] for item in incidencias_por_agente]
        
        # Resumen general de incidencias
        total_incidencias = CabIncidente_Model.objects.filter(**fecha_filter).count()
        
        # Obtener incidencias agrupadas por ubicación
        incidencias_por_ubicacion = CabIncidente_Model.objects.filter(**fecha_filter).values('agente__ubicacion__lugar').annotate(count=Count('id')).order_by('agente__ubicacion__lugar')
        
        # Extraer etiquetas (ubicaciones) y datos (conteo de incidencias)
        ubicaciones = [incidencia['agente__ubicacion__lugar'] for incidencia in incidencias_por_ubicacion]
        incidencias_por_ubicacion_data = [incidencia['count'] for incidencia in incidencias_por_ubicacion]
        
        # Agregar los datos al contexto
        context['ubicaciones'] = ubicaciones
        context['incidencias_por_ubicacion'] = incidencias_por_ubicacion_data
        context['total_incidencias'] = total_incidencias
        context['labels'] = labels
        context['data'] = data
        context['agentes'] = agentes
        context['incidencias'] = incidencias
        
        # Obtener los estados más recientes de los reportes
        subquery_estado = DetIncidente_Model.objects.filter(
            cabincidente=OuterRef('id')
        ).order_by('-hora').values('estado_incidente')[:1]  # Obtener el estado más reciente

        # Obtener la distribución de incidentes por estado (Notificado, En Proceso, Atendido, Cerrado)
        reportes_por_estado = CabIncidente_Model.objects.filter(**fecha_filter).annotate(
            estado_reciente=Subquery(subquery_estado)
        ).values('estado_reciente').annotate(cantidad=Count('estado_reciente')).order_by('estado_reciente')

        # Asegurarse que los estados tengan un valor, incluso si no hay incidentes en ese estado
        estados = ['N', 'E', 'A', 'C']  # N = Notificado, E = En Proceso, A = Atendido, C = Cerrado
        estados_labels = {
            'N': 'Notificado',
            'E': 'En Proceso',
            'A': 'Atendido',
            'C': 'Cerrado'
        }

        # Contar el total por cada estado
        estado_count = {estado: 0 for estado in estados}
        for reporte in reportes_por_estado:
            estado_count[reporte['estado_reciente']] = reporte['cantidad']

        # Generar los datos del gráfico de estados
        context['reportes_por_estado'] = [
            {'estado': estados_labels[estado], 'cantidad': estado_count[estado]} for estado in estados
        ]
        
        # Obtener la distribución de incidentes sin resolver (estados 'N' y 'E')
        reportes_sin_resolver = CabIncidente_Model.objects.filter(**fecha_filter).annotate(
            estado_reciente=Subquery(subquery_estado)
        ).filter(estado_reciente__in=['N', 'E'])  # Filtrar por estados 'N' y 'E')
        
        # Agrupar por mes y contar incidentes en estado 'N' o 'E'
        incidentes_por_mes = reportes_sin_resolver.annotate(
            mes=TruncMonth('fecha')  # Agrupar por mes de la fecha de creación
        ).values('mes').annotate(
            cantidad=Count('id')  # Contar incidentes en 'N' o 'E'
        ).order_by('mes')

        meses = []
        cantidad_sin_resolver = []  # Cantidad de incidentes sin resolver (N o E)

        # Crear listas separadas de meses y cantidades
        meses = [item['mes'].strftime('%B %Y') for item in incidentes_por_mes]
        cantidades = [item['cantidad'] for item in incidentes_por_mes]

        # Obtener los meses disponibles para el filtro (únicos y ordenados)
        meses_disponibles = incidentes_por_mes.values('mes').distinct().order_by('mes')
        
        # Si se selecciona un mes específico, filtrar por el mes correspondiente
        if mes_param != 'todos':
            incidentes_sin_resolver_filtrados = reportes_sin_resolver.filter(fecha__year=year, fecha__month=month)
            incidentes_por_mes = incidentes_sin_resolver_filtrados.annotate(
                mes=TruncMonth('fecha')
            ).values('mes').annotate(
                cantidad=Count('id')
            ).order_by('mes')
            # Actualizar meses y cantidades según el filtro
            meses = [item['mes'].strftime('%B %Y') for item in incidentes_por_mes]
            cantidades = [item['cantidad'] for item in incidentes_por_mes]
        
        # Combinar los meses y las cantidades en una lista de tuplas
        data = zip(meses, cantidades)
        
        # Pasar los datos al contexto
        context['datas'] = data
        context['meses_disponibles'] = meses_disponibles
        context['mes_param'] = mes_param

        return context
