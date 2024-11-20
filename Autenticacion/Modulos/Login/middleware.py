from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from Modulos.Login.utils import configuracion_completa, inactivar_superusuario

class ConfiguracionInicialMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if configuracion_completa() and request.user.is_superuser:
            # Inactivamos al superusuario globalmente si es necesario
            inactivar_superusuario()
             # Antes de cerrar la sesión, persiste el mensaje de éxito
            messages.success(request, "La configuración inicial ha sido completada y las credenciales utilizadas han sido desactivadas.")
            
            inactivar_superusuario()
            
            messages.success(request, "La configuración inicial ha sido completada y las credenciales utilizadas han sido desactivadas.")            
            
            logout(request)

            return redirect('login:login')

        response = self.get_response(request)
        return response
