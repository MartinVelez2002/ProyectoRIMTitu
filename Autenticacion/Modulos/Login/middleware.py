from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.timezone import now
from django.conf import settings
from datetime import datetime
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
            
            logout(request)

            return redirect('login:login')

        response = self.get_response(request)
        return response



class SessionTimeoutMiddleware:
    """
    Middleware para cerrar sesión después de un tiempo de inactividad definido en settings.SESSION_TIMEOUT.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Verifica si la última actividad existe en la sesión
            last_activity = request.session.get('last_activity')

            if last_activity:
                # Convierte la cadena ISO 8601 de vuelta a datetime
                last_activity_time = datetime.fromisoformat(last_activity)

                # Calcula la diferencia de tiempo en segundos
                elapsed_time = (now() - last_activity_time).total_seconds()

                # Cierra la sesión si el tiempo de inactividad excede el límite
                if elapsed_time > settings.SESSION_TIMEOUT:
                    messages.error(request,"Tiempo de inactividad superado. Vuelva a iniciar sesión.")
                    logout(request)
                    return redirect('login:login')  # Redirige al login

            # Actualiza la última actividad en cada solicitud (en formato ISO 8601)
            request.session['last_activity'] = now().isoformat()

        response = self.get_response(request)
        return response
    




class LoginAttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo afecta a la vista de login
        if request.path == '/accounts/login/' and request.method == 'POST':
            max_attempts = settings.MAX_LOGIN_ATTEMPTS
            lockout_time = settings.LOCKOUT_TIME

            login_attempts = request.session.get('login_attempts', 0)
            last_attempt_time = request.session.get('last_attempt_time')

            if last_attempt_time:
                last_attempt_time = datetime.fromisoformat(last_attempt_time)
                elapsed_time = (now() - last_attempt_time).total_seconds()

                if elapsed_time < lockout_time:
                    messages.error(request, f"Demasiados intentos fallidos. Intenta de nuevo en {int(lockout_time / 60)} minutos.")
                    return redirect('login:login')

            # Incrementar intentos solo si hubo un error en la autenticación
            if request.session.get('login_failed', False):
                login_attempts += 1
                request.session['login_attempts'] = login_attempts
                request.session['last_attempt_time'] = now().isoformat()

                if login_attempts >= max_attempts:
                    messages.error(request, f"Demasiados intentos fallidos. Bloqueando por {int(lockout_time / 60)} minutos.")
                    return redirect('login:login')

        # Continúa con la solicitud normalmente
        response = self.get_response(request)
        return response
