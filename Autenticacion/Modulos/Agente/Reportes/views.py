from django.urls import reverse_lazy, reverse
from .models import CabIncidente_Model, DetIncidente_Model
from django.views.generic import ListView, CreateView, UpdateView
from .forms import CabIncidente_Form, DetalleIncidente_Form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from Modulos.Coordinador.Calendario.models import TurnUsuario_Model

# Create your views here.
class Reportes_View(LoginRequiredMixin, ListView):
    model = CabIncidente_Model
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

class Reportes_Create(LoginRequiredMixin, CreateView):
    template_name = 'crear_reportes.html'
    success_url = reverse_lazy('reportes:listar_reportes')
    model = CabIncidente_Model
    form_class = CabIncidente_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario de Reportes'
        context['cancelar'] = reverse('reportes:listar_reportes')
        context['action_save'] = self.request.path
        # Instancia del formulario de detalle
        if self.request.POST:
            context['detalle_form'] = DetalleIncidente_Form(self.request.POST, self.request.FILES)
        else:
            context['detalle_form'] = DetalleIncidente_Form()
    

        return context


    def form_valid(self, form):
        # Recuperar el usuario actual
        current_user = self.request.user.id

        # Obtener el TurnUsuario_Model asociado al usuario
        try:
            turn_usuario = TurnUsuario_Model.objects.get(usuario__id=current_user)
        except TurnUsuario_Model.DoesNotExist:
            # Si no hay un TurnUsuario_Model para el usuario actual, manejar el error
            return self.form_invalid(form)

        # Recuperar el contexto y el formulario de detalle
        context = self.get_context_data()
        detalle_form = context['detalle_form']

        # Verificar si el formulario de detalle es válido
        if detalle_form.is_valid():
            # Guardar el formulario de CabIncidente_Model
            self.object = form.save(commit=False)
            self.object.agente = turn_usuario  # Asignar el TurnUsuario_Model al campo agente
            self.object.save()  # Asegúrate de guardar `self.object` antes de asociarlo a `detalle_instance`

            # Guardar la instancia de DetIncidente_Model asociada
            detalle_instance = detalle_form.save(commit=False)
            detalle_instance.cabincidente = self.object  # Asociar con la instancia de CabIncidente_Model
            detalle_instance.save()
            print("funcionando")
            return super().form_valid(form)
        else:
            # Si el formulario de detalle no es válido
            print("Errores en detalle_form:", detalle_form.errors)
            return self.form_invalid(form)


    def form_invalid(self, form):
        print("FORMULARIO INVÁLIDO")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class AdicionarDetalle(LoginRequiredMixin, CreateView):
    model = DetIncidente_Model
    form_class = DetalleIncidente_Form
    success_url = reverse_lazy('reportes:listar_reportes')
    

