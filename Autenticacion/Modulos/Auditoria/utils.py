from Modulos.Auditoria.models import AuditoriaUser
import socket

def save_audit(request, model, action):
    user = request.user
    client_address = ip_client_address(request)
    machine_name = obtener_nombre_maquina()
    
    # Obtener la descripción de la acción
    descripcion = get_action_description(model, action)
    
    # Registro en tabla de Auditoría
    tabla_auditoria = AuditoriaUser(
        usuario=user,
        tabla=model.__class__.__name__,
        registro_id=model.id,
        accion=action,
        nombre_maquina=machine_name,
        estacion=client_address,
        descripcion=descripcion  # Descripción de la acción
    )
    
    tabla_auditoria.save()

def get_action_description(model, action):
   
    if action == AuditoriaUser.AccionChoices.MODIFICAR:
        return f"Modificó un registro en la tabla {model.__class__.__name__} con ID {model.id}."
    elif action == AuditoriaUser.AccionChoices.CREAR:
        return f"Creó un nuevo registro en la tabla {model.__class__.__name__}."
    elif action == AuditoriaUser.AccionChoices.ELIMINAR:
        return f"Eliminó el registro con ID {model.id} de la tabla {model.__class__.__name__}."
    elif action == AuditoriaUser.AccionChoices.INACTIVAR:
        return f"Inactivó el registro con ID {model.id} de la tabla {model.__class__.__name__}."
    elif action == AuditoriaUser.AccionChoices.ACTIVAR:
        return f"Activó el registro con ID {model.id} de la tabla {model.__class__.__name__}."
    elif action == AuditoriaUser.AccionChoices.BLOQUEO:
        return f"Intentó realizar una acción bloqueada en la tabla {model.__class__.__name__} con ID {model.id}."
    elif action == AuditoriaUser.AccionChoices.ADVERTENCIA:
        return f"Recibió una advertencia al intentar realizar una acción en la tabla {model.__class__.__name__} con ID {model.id}."
    return ""


# Obtener el IP desde donde se esta accediendo
def ip_client_address(request):
    try:
        # caso de servidor externo
        client_address = request.META['HTTP_X_FORWARDED_FOR']
    except KeyError:
        # caso de localhost o 127.0.0.1
        client_address = request.META['REMOTE_ADDR']

    return client_address

# Obtener el nombre de la máquina
def obtener_nombre_maquina():
    try:
        return socket.gethostname()
    except Exception:
        return 'Unknown'
