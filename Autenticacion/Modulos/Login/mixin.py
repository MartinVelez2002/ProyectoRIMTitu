from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.views import View
from Modulos.Auditoria.models import AuditoriaUser
from Modulos.Auditoria.utils import save_audit
from Modulos.Login.models import Rol, Usuario
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from Modulos.Coordinador.Novedad.models import *


class CambiarEstadoMixin(View):
    model = None  
    redirect_url = None  

    def post(self, request, pk):
        if not self.model or not self.redirect_url:
            return redirect('login:index')  # Redirige si faltan parámetros obligatorios

        # Verificar si el usuario tiene rol asignado
        if request.user.rol is None:
            messages.error(request, "No tienes autorización para realizar esta operación. El único permiso disponible es para el registro.")
            return redirect(self.redirect_url)

        # Obtener el objeto según el modelo y pk
        objeto = get_object_or_404(self.model, pk=pk)

        # Verificar si el objeto es un Usuario o un Rol
        if isinstance(objeto, Usuario):
            is_coordinador = objeto.rol and objeto.rol.name == 'Coordinador'
            is_current_user = objeto == request.user
        elif isinstance(objeto, Rol):
            is_coordinador = objeto.name == 'Coordinador'
            is_current_user = False  # Un rol no puede ser el usuario actual
        else:
            is_coordinador = False
            is_current_user = False

        # Verificar si el rol del objeto es "Coordinador" y si el usuario actual tiene el rol de Coordinador
        if is_coordinador:
            if is_current_user:
                # No permitir que el usuario inactiva su propia cuenta
                messages.error(request, "No puedes inactivar tu propia cuenta.")
                action = AuditoriaUser.AccionChoices.BLOQUEO 
                save_audit(request, objeto, action=action)
                return redirect(self.redirect_url)  # Redirige a la vista de confirmación

            if isinstance(objeto, Rol):
                # No se puede eliminar el rol Coordinador
                messages.error(request, "No es posible eliminar el rol Coordinador.")
                action = AuditoriaUser.AccionChoices.BLOQUEO 
                save_audit(request, objeto, action=action)
                return redirect(self.redirect_url)  # Redirige a la vista de confirmación

            if isinstance(objeto, Usuario):
                # Advertencia si el usuario tiene el rol Coordinador
                messages.warning(request, "Estás a punto de cambiar el estado de un Coordinador, ¿estás seguro?")
                action = AuditoriaUser.AccionChoices.ADVERTENCIA 
                save_audit(request, objeto, action=action)
                return redirect('login:confirmar_accion_usuario', pk=objeto.pk)  # Redirige a la vista de confirmación del usuario

        # Manejo específico para TipoNovedad_Model
        if isinstance(objeto, TipoNovedad_Model):
            # Cambiar el estado del tipo de novedad
            objeto.estado = not objeto.estado
            objeto.save()

            # Si se inactiva el tipo, inactivar sus novedades relacionadas
            if not objeto.estado:
                relacionadas = Novedad_Model.objects.filter(tiponovedad=objeto, estado=True)
                relacionadas.update(estado=False)

            messages.success(request, f"El estado del Tipo de Novedad ha sido cambiado a {'Inactivo' if not objeto.estado else 'Activo'}.")
            return redirect(self.redirect_url)

        # Manejo específico para Novedad_Model
        if isinstance(objeto, Novedad_Model):
            if not objeto.estado:  # Intentando activar la novedad
                # Verificar si el TipoNovedad asociado está activo
                if not objeto.tiponovedad.estado:
                    messages.error(request, "Primero debe activar el Tipo de Novedad asociado para activar esta Novedad.")
                    return redirect(self.redirect_url)

            # Cambiar el estado de la novedad
            objeto.estado = not objeto.estado
            objeto.save()

            messages.success(request, f"El estado de la Novedad ha sido cambiado a {'Inactivo' if not objeto.estado else 'Activo'}.")
            return redirect(self.redirect_url)

        # Cambiar el estado del objeto para casos generales
        objeto.estado = not objeto.estado
        objeto.save()

        # Registrar la auditoría para el cambio de estado
        action = AuditoriaUser.AccionChoices.INACTIVAR if not objeto.estado else AuditoriaUser.AccionChoices.ACTIVAR
        save_audit(request, objeto, action=action)
                        
        messages.success(request, f"El estado del registro ha sido cambiado correctamente a {'Inactivo' if not objeto.estado else 'Activo'}.")
        return redirect(self.redirect_url)






class ConfirmarCambioEstadoView(View):
    model = None  
    redirect_url = None  

    def get(self, request, pk):
        # Verificar que el modelo esté definido
        if not self.model:
            messages.error(request, "No se ha especificado un modelo válido.")
            return redirect(self.redirect_url)  # Redirige a un listado por defecto si falta el URL

        # Obtener el objeto según el modelo y pk
        objeto = get_object_or_404(self.model, pk=pk)
        
        # Renderizar la plantilla de confirmación
        return render(request, 'confirmar_accion.html', {'objeto': objeto})

    def post(self, request, pk):
        # Verificar que el modelo esté definido
        if not self.model:
            messages.error(request, "No se ha especificado un modelo válido.")
            return redirect(self.redirect_url)

        # Obtener el objeto según el modelo y pk
        objeto = get_object_or_404(self.model, pk=pk)

        # Cambiar el estado del objeto
        objeto.estado = not objeto.estado
        objeto.save()

        # Registrar la auditoría para el cambio de estado
        action = AuditoriaUser.AccionChoices.INACTIVAR if not objeto.estado else AuditoriaUser.AccionChoices.ACTIVAR
        save_audit(request, objeto, action=action)
        
        # Mostrar el mensaje adecuado según el modelo
        mensaje_objeto = objeto.rol.name if self.model == Usuario else objeto.name
        messages.success(request, f"El estado de {'usuario' if self.model == Usuario else 'rol'} {mensaje_objeto} ha sido cambiado correctamente a {'Inactivo' if not objeto.estado else 'Activo'}.")

        # Redirigir a la URL especificada o al listado por defecto
        return redirect(self.redirect_url)
    




class RoleRequiredMixin:
    required_role = None  

    def dispatch(self, request, *args, **kwargs):
        if not request.user.rol or request.user.rol.name != self.required_role:
            return redirect(reverse('login:acceso_restringido'))
        return super().dispatch(request, *args, **kwargs)
    
    
