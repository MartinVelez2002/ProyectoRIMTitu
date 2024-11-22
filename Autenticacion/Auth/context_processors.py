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
            print("Buscando turno y ubicación del usuario...")
            turno_usuario = TurnUsuario_Model.objects.get(usuario=request.user, estado=True)
            context.update({
                'turno': turno_usuario.turno,  # Ajusta 'nombre' al campo correcto
                'ubicacion': turno_usuario.ubicacion,  # Ajusta 'nombre' al campo correcto
            })
        except TurnUsuario_Model.DoesNotExist:
            print("No se encontró un turno activo para este usuario.")
            context.update({
                'turno': 'No asignado',
                'ubicacion': 'No asignada',
            })

        print("Context generado:", context)
        return context

    # Contexto para usuarios no autenticados
    print("Usuario no autenticado o anónimo.")
    return {
        'nombre': '',
        'apellido': '',
        'turno': '',
        'ubicacion': '',
    }
