
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
from django.db.models import Q

from Modulos.Login.views import RoleRequiredMixin

class Novedad_View(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'novedad.html'
    context_object_name = 'novedad'
    model = Novedad_Model
    required_role = 'Coordinador'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('novedad:crear_novedad')
        context['title_table'] = 'Listado de Novedades'
        context['dir_search'] = self.request.path
        context['query'] = self.request.GET.get('query', '')
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            return self.model.objects.filter(
                Q(Descripcion__icontains=query) |
                Q(TipoNovedad__Descripcion__icontains=query)  # Reemplaza "tipo_novedad" con el nombre del campo de relación.
            )
        return self.model.objects.all()

    
class Novedad_Create(LoginRequiredMixin, RoleRequiredMixin,CreateView):
    model = Novedad_Model
    required_role = 'Coordinador'
    template_name = 'registrar_novedad.html'
    form_class = Novedad_form
    success_url = reverse_lazy('novedad:inicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Novedad'
        context['cancelar'] = reverse('novedad:inicio')
        context['action_save'] = self.request.path
        
        return context

        
    def form_invalid(self, form):
        messages.error(self.request, "Favor llenar el formulario")
        return super().form_invalid(form)

class Novedad_Update(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Novedad_Model
    required_role = 'Coordinador'
    template_name = 'registrar_novedad.html'
    success_url = reverse_lazy('novedad:inicio')
    form_class = Novedad_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'Edición de novedad'
        context['cancelar'] = reverse('novedad:inicio')
        
        return context
    
class TipoNovedad_View(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'tipNov.html'
    model = TipoNovedad_Model
    required_role = 'Coordinador'
    context_object_name = 'tipNov'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('novedad:crear_tipNov')
        context['title_table'] = 'Listado Tipo de Novedades'
        context['dir_search'] = self.request.path
        context['query'] = self.request.GET.get('query','')
                
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            return self.model.objects.filter(Descripcion__icontains=query)
        else:
            return self.model.objects.all()
    
class TipoNovedad_Create(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = TipoNovedad_Model
    required_role = 'Coordinador'
    template_name = 'registrar_tipNovedad.html'
    form_class = TipoNovedad_form
    success_url = reverse_lazy('novedad:inicio_tipoNov')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario: Tipo de Novedad'
        context['cancelar'] = reverse('novedad:inicio_tipoNov')
        context['action_save'] = self.request.path
        
        return context



class TipoNovedad_Update(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = TipoNovedad_Model
    required_role = 'Coordinador'
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
    model = None  
    redirect_url = None   

    def post(self, request, pk):
        if not self.model or not self.redirect_url:
            return redirect('')   
        
        objeto = get_object_or_404(self.model, pk=pk)
        
        if objeto.Estado:
            objeto.Estado = False 
        else:
            objeto.Estado = True  
        objeto.save()
      
        return redirect(self.redirect_url)
 
    
    
    
class InactivarActivarTipoNovedadView(CambiarEstadoMixin):
    model = TipoNovedad_Model
    redirect_url = 'novedad:inicio_tipoNov'  

class InactivarActivarNovedadView(CambiarEstadoMixin):
    model = Novedad_Model
    redirect_url = 'novedad:inicio' 