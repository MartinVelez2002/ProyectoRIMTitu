
from Modulos.Coordinador.Novedad.models import TipoNovedad_Model, Novedad_Model
from Modulos.Coordinador.Novedad.forms import Novedad_form, TipoNovedad_form
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from Modulos.Auditoria.models import AuditoriaUser
from Modulos.Auditoria.utils import save_audit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View


class Novedad_View(LoginRequiredMixin, ListView):
    template_name = 'novedad.html'
    context_object_name = 'novedad'
    model = Novedad_Model
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('novedad:crear_novedad')
        context['title_table'] = 'Listado de Novedades'
        return context
    
class Novedad_Create(LoginRequiredMixin, CreateView):
    model = Novedad_Model
    template_name = 'registrar_novedad.html'
    form_class = Novedad_form
    success_url = reverse_lazy('novedad:inicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Novedad'
        context['cancelar'] = reverse('novedad:inicio')
        context['action_save'] = self.request.path
        return context

    def form_valid(self, form):
        novedad = form.save(commit=False)
        novedad.Estado = True
        novedad.save()
        # Primero, guarda la novedad llamando a form_valid del padre
        response = super().form_valid(form) 
        # Ahora `self.object` está disponible y se puede usar
        novedad = self.object 
        # Registrar en auditoría la acción de creación
        save_audit(self.request, novedad, action=AuditoriaUser.AccionChoices.CREAR)  
        return response
        
    def form_invalid(self, form):
        messages.error(self.request, "Favor llenar el formulario")
        return super().form_invalid(form)

class Novedad_Update(LoginRequiredMixin, UpdateView):
    model = Novedad_Model
    template_name = 'registrar_novedad.html'
    success_url = reverse_lazy('novedad:inicio')
    form_class = Novedad_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'Edición de novedad'
        context['cancelar'] = reverse('novedad:inicio')
        
        return context
    
class TipoNovedad_View(LoginRequiredMixin, ListView):
    template_name = 'tipNov.html'
    model = TipoNovedad_Model
    context_object_name = 'tipNov'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('novedad:crear_tipNov')
        context['title_table'] = 'Listado Tipo de Novedades'
                
        return context
    
class TipoNovedad_Create(LoginRequiredMixin, CreateView):
    model = TipoNovedad_Model
    template_name = 'registrar_tipNovedad.html'
    form_class = TipoNovedad_form
    success_url = reverse_lazy('novedad:inicio_tipoNov')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Tipo de Novedad'
        context['cancelar'] = reverse('novedad:inicio_tipoNov')
        context['action_save'] = self.request.path
        
        return context
    
    def form_valid(self, form):
        tipNov = form.save(commit = False)
        tipNov.Estado = True
        tipNov.save()
        return super().form_valid(form)


class TipoNovedad_Update(LoginRequiredMixin, UpdateView):
    model = TipoNovedad_Model
    template_name = 'registrar_tipNovedad.html'
    success_url = reverse_lazy("novedad:inicio_tipoNov")
    form_class = TipoNovedad_form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'Edición del tipo de novedad'
        context['cancelar'] = reverse('novedad:inicio_tipoNov')
        

        return context
    
    


class CambiarEstadoMixin(View):
    model = None  # Este atributo debe ser sobrescrito en cada vista hija
    redirect_url = None   # URL de redirección según el modelo

    def post(self, request, pk):
        if not self.model or not self.redirect_url:
            return redirect('')   # Si no se ha definido un modelo, redirigir

        # Obtener el objeto según el modelo y pk
        objeto = get_object_or_404(self.model, pk=pk)

        # Cambiar el estado (si está activo, se inactiva; si está inactivo, se activa)
        if objeto.Estado:
            objeto.Estado = False  # Inactiva el objeto
        else:
            objeto.Estado = True  # Activa el objeto
        objeto.save()
      
        return redirect(self.redirect_url)
 
    
    
    
class InactivarActivarTipoNovedadView(CambiarEstadoMixin):
    model = TipoNovedad_Model
    redirect_url = 'novedad:inicio_tipoNov'  # Redirección específica para TipoNovedad_Model

class InactivarActivarNovedadView(CambiarEstadoMixin):
    model = Novedad_Model
    redirect_url = 'novedad:inicio'  # Redirección específica para Novedad_Model