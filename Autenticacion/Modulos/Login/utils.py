from django.core.exceptions import ValidationError




def validar_cedula(cedula):
    cedula = str(cedula)
    if not cedula.isdigit():
        raise ValidationError('La cédula debe contener solo datos numéricos.')
    
    longitud = len(cedula)
    if longitud != 10:
        raise ValidationError('Cantidad de dígitos incorrecta.')
    
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    
    for i in range(9):
        digito = int(cedula[i])
        coeficiente = coeficientes[i]
        producto = digito* coeficiente
        if producto > 9:
            producto -= 9
        total += producto
        
    digito_verificador = (total * 9) % 10
    if digito_verificador != int(cedula[9]):
        raise ValidationError('La cédula no es válida.')
    
    

