from Modulos.Login.models import Rol, Usuario

    

def configuracion_completa():
    """Verifica si el rol 'Coordinador' y el usuario asociado existen."""
    rol = Rol.objects.filter(name='Coordinador', estado=True).exists()
    usuario_coordinador = Usuario.objects.filter(rol__name='Coordinador', estado=True).exists()

    return rol and usuario_coordinador

def inactivar_superusuario():
    """Inactiva el superusuario después de la configuración inicial."""
    
    superusuario = Usuario.objects.filter(is_superuser=True, estado=True).first()
    if superusuario:
        superusuario.estado = False
        superusuario.save()
        print(f"Superusuario {superusuario.username} inactivado correctamente.")