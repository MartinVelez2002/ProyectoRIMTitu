from Modulos.Auditoria.models import AuditoriaUser
import socket

def save_audit(request, model, action):
    user = request.user
    client_address = ip_client_address(request)
    machine_name = obtener_nombre_maquina()
    
    
    # Registro en tabla de Auditoría
    tabla_auditoria = AuditoriaUser(
        usuario=user,
        tabla=model.__class__.__name__,
        registro_id=model.id,
        accion=action,
        nombre_maquina=machine_name,
        estacion=client_address
    )
    
    tabla_auditoria.save()

# Obtener el IP desde donde se esta accediendo
def ip_client_address(request):
    try:
        # case server externo
        client_address = request.META['HTTP_X_FORWARDED_FOR']
    except:
        # case localhost o 127.0.0.1
        client_address = request.META['REMOTE_ADDR']

    return client_address


# Obtener el nombre de la máquina
def obtener_nombre_maquina():
    try:
        return socket.gethostname()
    except Exception:
        return 'Unknown'