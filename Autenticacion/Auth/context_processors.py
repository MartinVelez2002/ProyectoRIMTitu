from django.contrib.auth.models import AnonymousUser
from Modulos.Coordinador.Calendario.models import TurnUsuario_Model
def user_info(request):
    if request.user and not isinstance(request.user, AnonymousUser):
        return {
            'nombre': request.user.nombre,  # O usa 'nombre' si lo tienes en tu modelo
            'apellido': request.user.apellido,  # O 'apellido'
        }
     # Verificamos si el usuario es un agente
    if hasattr(request.user, 'rol') and request.user.rol == 'agente':  # Cambia 'rol' si tu modelo usa otro nombre
        # Recuperamos turno y ubicación del usuario (asociados con TurnUsuario_Model)
        try:
            turno_usuario = TurnUsuario_Model.objects.get(usuario=request.user, estado=True)
            context.update({
                'turno': turno_usuario.turno.nombre,  # Cambia 'nombre' por el campo correspondiente del modelo Turno_Model
                'ubicacion': turno_usuario.ubicacion.nombre,  # Cambia 'nombre' por el campo correspondiente del modelo Ubicacion_Model
            })
        except TurnUsuario_Model.DoesNotExist:
            # Si no tiene asignado un turno activo
            context.update({
                'turno': 'No asignado',
                'ubicacion': 'No asignada',
            })

    return context
    return {'nombre': '', 'apellido': ''}  # Para usuarios no autenticados
