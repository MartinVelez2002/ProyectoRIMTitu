from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.timezone import now
from django.conf import settings
from datetime import datetime
from Modulos.Login.models import Usuario
from Modulos.Login.utils import configuracion_completa, inactivar_superusuario
from Modulos.Login.models import Usuario


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
    """
    Middleware para bloquear intentos de inicio de sesión después de varios fallos consecutivos.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bloquear solo en la vista de inicio de sesión
        if request.path == '/accounts/login/' and request.method == 'POST':

            # Obtener el identificador del usuario (nombre de usuario)
            username = request.POST.get('username', None)

            # Número máximo de intentos permitidos
            max_attempts = settings.MAX_LOGIN_ATTEMPTS
            # Tiempo de bloqueo en segundos
            lockout_time = settings.LOCKOUT_TIME

            if username:
                # Crear claves de sesión específicas para cada usuario
                login_attempts_key = f'login_attempts_{username}'
                last_attempt_time_key = f'last_attempt_time_{username}'

                # Obtener el contador de intentos fallidos y el timestamp del último intento fallido
                login_attempts = request.session.get(login_attempts_key, 0)
                last_attempt_time = request.session.get(last_attempt_time_key)

                # Verificar si el nombre de usuario es válido
                try:
                    user = Usuario.objects.get(username=username)
                except Usuario.DoesNotExist:
                    # Si el nombre de usuario no existe, lo tratamos como un intento fallido
                    login_attempts += 1
                    request.session[login_attempts_key] = login_attempts
                    request.session[last_attempt_time_key] = now().isoformat()
                    messages.error(request, "El nombre de usuario no existe.")
                    return redirect('login:login')

                # Se verifica si hay un tiempo de bloqueo almacenado
                if last_attempt_time:
                    # Convertimos el timestamp almacenado en sesión a un objeto datetime
                    last_attempt_time = datetime.fromisoformat(last_attempt_time)
                    elapsed_time = (now() - last_attempt_time).total_seconds()

                    # Si el tiempo de bloqueo no ha expirado y los intentos han sido superados
                    if elapsed_time < lockout_time and login_attempts >= max_attempts:
                        messages.error(request, f"El tiempo de bloqueo no ha expirado, por favor, sea paciente.")
                        return redirect('login:login')  # Redirige a la página de inicio de sesión

                    # Si el tiempo de bloqueo ha expirado, restablecer los intentos
                    if elapsed_time >= lockout_time:
                        login_attempts = 0
                        request.session[login_attempts_key] = login_attempts  # Restablecer el valor en la sesión

                # Si el login falló (esto debe manejarlo el sistema de autenticación de Django)
                if request.session.get('login_failed', False):
                    login_attempts += 1
                    request.session[login_attempts_key] = login_attempts
                    request.session[last_attempt_time_key] = now().isoformat()

                    # Si se ha superado el número máximo de intentos
                    if login_attempts >= max_attempts:
                        messages.error(request, f"Superaste el número de intentos para iniciar sesión. Intenta de nuevo en {int(lockout_time / 60)} minutos.")
                        return redirect('login:login')
        # Continúa con la solicitud normalmente
        response = self.get_response(request)
        return response
