from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from Modulos.Auditoria.models import AuditoriaUser
from Modulos.Auditoria.utils import save_audit


class CambiarEstadoMixin(View):
    model = None  
    redirect_url = None  

    def post(self, request, pk):
        if not self.model or not self.redirect_url:
            return redirect('')  

        # Obtener el objeto según el modelo y pk
        objeto = get_object_or_404(self.model, pk=pk)

        if objeto.estado:
            objeto.estado = False 
        else:
            objeto.estado = True
        objeto.save()

         # Registrar la auditoría para el cambio de estado
        save_audit(request, objeto, action=AuditoriaUser.AccionChoices.INACTIVAR if objeto.estado == False else AuditoriaUser.AccionChoices.ACTIVAR)
        
        return redirect(self.redirect_url)
    

class RoleRequiredMixin:
    required_role = None  

    def dispatch(self, request, *args, **kwargs):
        if not request.user.rol or request.user.rol.name != self.required_role:
            return redirect(reverse('login:acceso_restringido'))
        return super().dispatch(request, *args, **kwargs)
    
    
