from django.urls import reverse_lazy, reverse

from Modulos.Login.mixin import RoleRequiredMixin
from .models import CabIncidente_Model
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
    
    def get_queryset(self):
        usuario_id = self.request.user.id  # Obtenemos el ID del usuario logueado
        return CabIncidente_Model.objects.filter(agente__usuario__id=usuario_id).prefetch_related('detalles')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('reportes:crear_reporte')
        context['title_table'] = 'Listado de mis Reportes'
        
        return context




class Reportes_Create(LoginRequiredMixin, RoleRequiredMixin, CreateView):
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
        current_user = self.request.user

        # Intentar obtener o crear el TurnUsuario_Model del usuario actual
        turn_usuario, created = TurnUsuario_Model.objects.get_or_create(usuario=current_user)

        if not turn_usuario:
            # Si no se encuentra un TurnUsuario_Model válido, retorna como inválido
            return self.form_invalid(form)

        # Recuperar el formulario de detalle desde el contexto
        context = self.get_context_data()
        detalle_form = context['detalle_form']

        # Validar el formulario de detalle
        if detalle_form.is_valid():
            # Guardar la cabecera del incidente
            self.object = form.save(commit=False)
            self.object.agente = turn_usuario
            self.object.save()

            # Guardar el detalle del incidente asociado a la cabecera
            detalle_instance = detalle_form.save(commit=False)
            detalle_instance.cabincidente = self.object
            detalle_instance.save()

            return super().form_valid(form)
        else:
            # Si el formulario de detalle es inválido, re-renderizar el template con errores
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Añadir los errores de ambos formularios al contexto
        context = self.get_context_data(form=form)
        return self.render_to_response(context)















# class AdicionarDetalle(LoginRequiredMixin, CreateView):
#     model = DetIncidente_Model
#     form_class = DetalleIncidente_Form
#     template_name = 'adicionar_detalle.html'
#     success_url = reverse_lazy('reportes:listar_reportes')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Pasar el ID de la cabecera al contexto
#         context['cabecera_id'] = self.kwargs['cabecera_id']
#         return context

#     def form_valid(self, form):
#         cabecera_id = self.kwargs['cabecera_id']
#         form.instance.cabecera_id = cabecera_id
#         return super().form_valid(form)

    

