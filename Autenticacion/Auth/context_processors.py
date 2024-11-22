from django.contrib.auth.models import AnonymousUser
from Modulos.Coordinador.Calendario.models import TurnUsuario_Model

def user_info(request):
    if request.user and not isinstance(request.user, AnonymousUser):
        # Inicializamos el contexto básico
        context = {
            'nombre': request.user.nombre,
            'apellido': request.user.apellido,
        }

        try:
            
            turno_usuario = TurnUsuario_Model.objects.get(usuario=request.user, estado=True)
            context.update({
                'turno': turno_usuario.turno,  # Ajusta 'nombre' al campo correcto
                'ubicacion': turno_usuario.ubicacion,  # Ajusta 'nombre' al campo correcto
            })
        except TurnUsuario_Model.DoesNotExist:
            context.update({
                'turno': 'No asignado',
                'ubicacion': 'No asignada',
            })
        return context

    # Contexto para usuarios no autenticados
    return {
        'nombre': '',
        'apellido': '',
        'turno': '',
        'ubicacion': '',
    }
