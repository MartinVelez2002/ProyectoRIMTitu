from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.db.models import Q
from Modulos.Coordinador.Ubicacion.models import Ubicacion_Model
from Modulos.Coordinador.Ubicacion.forms import Ubicacion_Form
from Modulos.Login.mixin import CambiarEstadoMixin, RoleRequiredMixin



class Ubicacion_View(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Ubicacion_Model
    required_role = 'Coordinador'
    template_name = 'ubicacion.html'
    context_object_name = 'ubicacion'     
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('ubicacion:crear_ubicacion')
        context['title_table'] = 'Listado de Ubicaciones'
        context['dir_search'] = self.request.path
        context['query'] = self.request.GET.get('query', '')
        return context

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return self.model.objects.filter(
                Q(lugar__icontains = query) |
                Q(sector__icontains = query)
            )
        return self.model.objects.all()

class Ubicacion_Create(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Ubicacion_Model
    required_role = 'Coordinador'
    template_name = 'registrar_ubicacion.html'
    form_class = Ubicacion_Form
    success_url = reverse_lazy('ubicacion:inicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Ubicación'
        context['cancelar'] = reverse('ubicacion:inicio')
        context['action_save'] = self.request.path
        context['google_maps_api_key'] = settings.GOOGLE_API_KEY
        return context
    
class Ubicacion_Update(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Ubicacion_Model
    required_role = 'Coordinador'
    template_name = 'registrar_ubicacion.html'
    form_class = Ubicacion_Form
    success_url = reverse_lazy('ubicacion:inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edición de la ubicación'
        context['cancelar'] = reverse('ubicacion:inicio')
        context['action_save'] = self.request.path
        context['google_maps_api_key'] = settings.GOOGLE_API_KEY

        return context



    
    
class InactivarActivarUbicacionView(CambiarEstadoMixin):
    model = Ubicacion_Model
    redirect_url = 'ubicacion:inicio'  # Redirección específica para TipoNovedad_Model
