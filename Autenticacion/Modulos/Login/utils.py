from django.core.exceptions import ValidationError

from Modulos.Login.models import Rol, Usuario



# def validar_campo(value):
#     if not value.isalpha():
#         raise ValidationError('El nombre del rol solo puede contener letras sin caracteres especiales ni números.')



# def validar_cedula(cedula):
#     cedula = str(cedula)
#     if not cedula.isdigit():
#         raise ValidationError('La cédula debe contener solo datos numéricos.')
    
#     longitud = len(cedula)
#     if longitud != 10:
#         raise ValidationError('Cantidad de dígitos incorrecta.')
    
#     coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
#     total = 0
    
#     for i in range(9):
#         digito = int(cedula[i])
#         coeficiente = coeficientes[i]
#         producto = digito* coeficiente
#         if producto > 9:
#             producto -= 9
#         total += producto
        
#     digito_verificador = (total * 9) % 10
#     if digito_verificador != int(cedula[9]):
#         raise ValidationError('La cédula no es válida.')
    
    

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