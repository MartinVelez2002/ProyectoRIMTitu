from django.contrib.auth.models import AnonymousUser
from Modulos.Coordinador.Calendario.models import TurnUsuario_Model

def user_info(request):
    # Inicializamos el contexto con valores predeterminados
    context = {
        'nombre': '',
        'apellido': '',
        'turno': '',
        'ubicacion': '',
    }
    
    # Verificamos si el usuario está autenticado
    if request.user and not isinstance(request.user, AnonymousUser):
        # Intentamos obtener el nombre y apellido del usuario
        try:
            context['nombre'] = getattr(request.user, 'nombre', '')
            context['apellido'] = getattr(request.user, 'apellido', '')
        except AttributeError:
            # Si los campos no existen, dejamos los valores predeterminados
            pass
        
        # Verificamos si el usuario tiene el rol de agente
        if hasattr(request.user, 'rol') and getattr(request.user, 'rol', '') == 'agente':
            # Intentamos recuperar el turno y la ubicación
            try:
                turno_usuario = TurnUsuario_Model.objects.get(usuario=request.user, estado=True)
                context.update({
                    'turno': getattr(turno_usuario.turno, 'nombre', 'No asignado'),
                    'ubicacion': getattr(turno_usuario.ubicacion, 'nombre', 'No asignada'),
                })
            except TurnUsuario_Model.DoesNotExist:
                # Si no se encuentra un turno activo
                context['turno'] = 'No asignado'
                context['ubicacion'] = 'No asignada'

    return context
