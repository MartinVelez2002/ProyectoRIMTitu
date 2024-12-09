from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.contrib import messages
from Modulos.Login.mixin import RoleRequiredMixin
from .models import CabIncidente_Model, DetIncidente_Model
from django.views.generic import ListView, CreateView
from .forms import CabIncidente_Form, DetalleIncidente_Form
from django.contrib.auth.mixins import LoginRequiredMixin
from Modulos.Coordinador.Calendario.models import TurnUsuario_Model

# Create your views here.
class Reportes_View(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = CabIncidente_Model
    required_role = 'Agente'
    template_name = 'listar_reportes.html'
    paginate_by = 5
    context_object_name = 'rep'
    
    def post(self, request, *args, **kwargs):
        incidente_id = request.POST.get('incidente_id')  # Obtener el ID del incidente (de un campo oculto o similar)
        try:
            incidente = CabIncidente_Model.objects.get(id=incidente_id)  # Obtener el incidente
        except CabIncidente_Model.DoesNotExist:
            messages.error(request, "El incidente especificado no existe.")
            return redirect('reportes:listar_reportes')  # Redirigir si no se encuentra el incidente
        
       
        
        incidente = CabIncidente_Model.objects.get(id=incidente_id)  # Obtener el incidente
        nuevo_estado = request.POST.get("nuevo_estado")
        descripcion = request.POST.get("descripcion")
        evidencia = request.FILES.get("evidencia")
        comentarios = request.POST.get("comentarios")# Obtener archivo de evidencia (si se carga)


        # Validar que el estado ya no exista en los detalles del incidente
        if incidente.detalles.filter(estado_incidente=nuevo_estado).exists():
            messages.error(request, "No es posible cambiar el estado del incidente a un estado pasado.")
            return redirect('reportes:listar_reportes')
        
        
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

        return redirect('reportes:listar_reportes')  # Asegúrate de que la URL esté correcta
    
    def get_queryset(self):
        usuario_id = self.request.user.id  # Obtenemos el ID del usuario logueado
        try:
            return CabIncidente_Model.objects.filter(
                agente__usuario__id=usuario_id
            ).select_related('agente').prefetch_related('detalles').order_by('-fecha', '-id')
        except Exception as e:
            messages.error(self.request, f"Error al cargar reportes: {e}")
            return CabIncidente_Model.objects.none()
        
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('reportes:crear_reporte')
        context['title_table'] = 'Listado de mis Reportes'
         # Pasar el estado del incidente al template
        context['nuevo_estado'] = self.request.POST.get('nuevo_estado', None)
        return context





class IncidenteCreateView(LoginRequiredMixin, RoleRequiredMixin,CreateView):
    template_name = 'crear_reportes.html'
    required_role = 'Agente'
    success_url = reverse_lazy('reportes:listar_reportes')
    model = CabIncidente_Model
    form_class = CabIncidente_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte de Incidencia'
        context['cancelar'] = reverse('reportes:listar_reportes')
        context['action_save'] = self.request.path

        # Añadir el formulario de detalle al contexto
        if self.request.POST:
            context['detalle_form'] = DetalleIncidente_Form(self.request.POST, self.request.FILES)
        else:
            context['detalle_form'] = DetalleIncidente_Form()

        return context


    def form_valid(self, form):
        """Maneja la lógica de guardado para ambos formularios."""
        current_user = self.request.user.id

        # Intentar obtener o crear el TurnUsuario_Model del usuario actual
        turn_usuario, created = TurnUsuario_Model.objects.get_or_create(usuario__id=current_user, estado = True)

        if not turn_usuario:
            # Si no se encuentra un TurnUsuario_Model válido, retorna como inválido
            return self.form_invalid(form)


        context = self.get_context_data()
        detalle_form = context['detalle_form']

        if detalle_form.is_valid():
            try:
                with transaction.atomic():
                    # Guardar cabecera del incidente
                    cab_incidente = form.save(commit=False)
                    cab_incidente.agente = turn_usuario
                    cab_incidente.save()

                    # Guardar detalle del incidente
                    detalle = detalle_form.save(commit=False)
                    detalle.cabincidente = cab_incidente
                    detalle.save()

                    messages.success(self.request, "Reporte creado exitosamente.")
                    return super().form_valid(form)
            except Exception as e:
                messages.error(self.request, f"Error al guardar el reporte: {e}")
                return self.form_invalid(form)
        else:
            messages.error(self.request, "Corrige los errores en el formulario de detalle.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Muestra errores cuando alguno de los formularios no es válido."""
        messages.error(self.request, "Corrige los errores en el formulario.")
        return super().form_invalid(form)








    

