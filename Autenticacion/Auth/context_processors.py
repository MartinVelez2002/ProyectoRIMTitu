from django.contrib.auth.models import AnonymousUser
from Modulos.Coordinador.Calendario.models import TurnUsuario_Model

def user_info(request):
    if request.user and not isinstance(request.user, AnonymousUser):
        # Datos básicos
        context = {
            'nombre': request.user.nombre,  # Asumiendo que tu modelo de usuario tiene 'nombre'
            'apellido': request.user.apellido,  # Asumiendo que tu modelo de usuario tiene 'apellido'
        }
        print("PREVIO AL IF CONDICIONAL")
        print(request.user.rol)
        # Verificamos si el usuario es un agente
        if hasattr(request.user, 'rol') and request.user.rol == 'Agente':  # Cambia 'rol' si tu modelo usa otro nombre
            # Recuperamos turno y ubicación del usuario (asociados con TurnUsuario_Model)
            print("PREVIO AL TRY")
            try:
                print("ENTRA POR EL TRY")
                print(TurnUsuario_Model.objects.all())
                turno_usuario = TurnUsuario_Model.objects.get(usuario=request.user, estado=True)
                context.update({
                    'turno': turno_usuario.turno,  # Cambia 'nombre' por el campo correspondiente del modelo Turno_Model
                    'ubicacion': turno_usuario.ubicacion,  # Cambia 'nombre' por el campo correspondiente del modelo Ubicacion_Model
                })
            except TurnUsuario_Model.DoesNotExist:
                # Si no tiene asignado un turno activo
                context.update({
                    'turno': 'No asignado',
                    'ubicacion': 'No asignada',
                })
        print(context)
        return context

    # Datos para usuarios no autenticados o anónimos
    return {
        'nombre': '',
        'apellido': '',
        'turno': '',
        'ubicacion': ''
    }
