import re
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string 
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import FormView
from Modulos.Login.forms import FormularioLogin, FormularioRegistro, CambiarPasswordForm, ForgetPasswordForm
from Modulos.Login.models import Usuario
# Create your views here.

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('login:index')
    change_password_url = reverse_lazy('login:cambiar_clave')
    
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)


    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        user = authenticate(request=self.request, username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            
            if user.primera_sesion:
                return HttpResponseRedirect(self.change_password_url)
            return super(Login, self).form_valid(form)
        return self.form_invalid(form)
        
    def form_invalid(self, form):
        # Añadir el mensaje de error cuando el formulario es inválido
        messages.error(self.request, "Credenciales inválidas. Intente nuevamente.")
        return super(Login, self).form_invalid(form)


def LogoutUsuario(request):
    if request.user.is_authenticated:
        # Cierra la sesión del usuario actual
        logout(request)
        # Opcional: Eliminar la sesión de la base de datos si deseas mantener el control
        Session.objects.filter(session_key=request.session.session_key).delete()

    return redirect('login:login')  




class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'





class RegistroView(LoginRequiredMixin, CreateView):
    template_name = 'registro.html'
    model = Usuario
    form_class = FormularioRegistro
    success_url = reverse_lazy('login:registro')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Personal'
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)    
        if form.is_valid():
            # Usar el método create_user de UsuarioManager
            nuevo_usuario = Usuario.objects.create_user(
                email=form.cleaned_data.get('email'),
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'),
                cedula=form.cleaned_data.get('cedula'),
                rol=form.cleaned_data.get('rol'),          
               
            )
            
            # Preparar y enviar el correo
            subject = 'Bienvenido a nuestro sistema'
            email_template_name = "credenciales.html"
            context = {
                "user": nuevo_usuario.username,
                "email": nuevo_usuario.email,
                "password": form.cleaned_data.get('password1'),
                "site_name": 'Municipio de Milagro',
                
            }
            
           
            html_message = render_to_string(email_template_name,context)
            
            send_mail(
                subject,  
                '',
                settings.DEFAULT_FROM_EMAIL,  # Cambia esto por el correo desde el que envías
                [nuevo_usuario.email],
                fail_silently=False,
                html_message=html_message
            )
            
            
            messages.success(request, 'Usuario registrado con éxito.')
            return redirect(self.success_url)
            
        else:  
            messages.error(request,'El formulario no ha procesado la información correctamente.')
            return render(request, self.template_name, {'form': form})







class ForgetPassword(FormView):
    template_name = 'olvidar_clave.html'  # Tu plantilla de olvidar clave
    form_class = ForgetPasswordForm
    success_url = reverse_lazy('login:olvidar_clave')  # Quedarse en la misma página tras el envío
    
    def form_valid(self, form):
        correo = form.cleaned_data.get('correo')
        usuario = Usuario.objects.filter(email=correo).first()
        if usuario:
            subject = "Restablecer tu contraseña"
            email_template_name = "correo_enviado.html"
            context = {
                "email": usuario.email,
                "domain": self.request.META['HTTP_HOST'],
                "site_name": 'Municipio de Milagro',
                "uid": urlsafe_base64_encode(force_bytes(usuario.pk)),
                "user": usuario,
                "token": default_token_generator.make_token(usuario),
                "protocol": 'https' if self.request.is_secure() else 'http',
            }
            
           # Generar el contenido HTML del correo
            html_message = render_to_string(email_template_name, context)

            # Enviar el correo usando solo el HTML
            send_mail(
                subject, 
                '',  # El mensaje de texto plano lo dejamos vacío si no quieres enviar uno
                settings.DEFAULT_FROM_EMAIL, 
                [usuario.email], 
                fail_silently=False, 
                html_message=html_message  # Versión HTML del correo
            )
            messages.success(self.request, 'Correo enviado. Revisa tu bandeja de entrada.')
        else:
            messages.error(self.request, '¡El correo ingresado no está registrado!')
            return super().form_valid(form)

    def form_invalid(self, form):
        # Aquí puedes manejar lo que ocurre si el formulario es inválido.
        messages.error(self.request, 'Por favor, ingrese un correo válido.')
        return super().form_invalid(form)




class ChangePasswordFirstSession(LoginRequiredMixin, FormView):
    template_name = 'cambiar_clave_primera_sesion.html'  # Cambia por el nombre de tu plantilla
    form_class = CambiarPasswordForm  # Usa tu formulario personalizado
    success_url = reverse_lazy('login:login')  # Redirige al usuario a la página de inicio de sesión después del cambio
    
    
    def form_valid(self, form):
        if not self.is_password_valid(form):
            return self.form_invalid(form)
        
        # Si todo es válido, se procesa el cambio de contraseña
        self.change_user_password(form.cleaned_data.get('password1'))
        messages.success(self.request, "Tu contraseña ha sido cambiada exitosamente.")
        return super().form_valid(form)
    
    
    def form_invalid(self, form): 
        return super().form_invalid(form)
    
    
    def is_password_valid(self, form):
        password_actual = form.cleaned_data.get('password_actual')
        password1 = form.cleaned_data.get('password1')

        if not self.request.user.check_password(password_actual):
            messages.error(self.request, 'La contraseña actual es incorrecta.')
            return False

        if not self.password_meets_criteria(password1):
            messages.error(self.request, 'La nueva contraseña no cumple con los requisitos de seguridad.')
            return False

        return True
       
    
    def password_meets_criteria(self, password):
        """
        Verifica que la contraseña cumpla con los siguientes criterios:
        1. Al menos un carácter en minúscula.
        2. Al menos un carácter en mayúscula.
        3. Al menos un número.
        4. Al menos un carácter especial.
        5. Al menos 8 caracteres.
        """
        lower = re.compile('(?=.*[a-z])')
        upper = re.compile('(?=.*[A-Z])')
        number = re.compile('(?=.*[0-9])')
        special = re.compile('(?=.*[!@#\\$%\\^&\\*])')
        length = re.compile('(?=.{8,})')

        if (lower.match(password) and
            upper.match(password) and
            number.match(password) and
            special.match(password) and
            length.match(password)):
            return True
        return False
    
    
    def change_user_password(self, new_password):
        # Lógica para cambiar la contraseña del usuario
        user = self.request.user
        user.set_password(new_password)
        user.primera_sesion = False
        user.save() 
    

class PasswordResetConfirmView(View):
    template_name = 'cambiar_clave.html'  
    form_class = CambiarPasswordForm

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            usuario = Usuario.objects.get(pk=uid)  # Modelo Usuario y extraer la instancia del usuario
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            usuario = None

        if usuario is not None and default_token_generator.check_token(usuario, token):
            form = self.form_class()
            return render(request, self.template_name, {'form': form, 'validlink': True, 'uid': uidb64, 'token': token})
        else:
            messages.error(request, 'El enlace de restablecimiento de contraseña es inválido o ha expirado.')
            return redirect('login:olvidar_clave')  # Redirigir a la página de olvidar contraseña


   
    def post(self, request, uidb64, token):  
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            usuario = Usuario.objects.get(pk=uid)  
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            messages.error(request, 'El usuario no existe o el enlace es inválido.')
            return redirect('login:olvidar_clave')  # Redirigir a la página de olvidar contraseña


        form = self.form_class(request.POST)
        if form.is_valid():
            nueva_contraseña = form.cleaned_data.get('password1')
            
            # Validar criterios de contraseña
            if not self.password_meets_criteria(nueva_contraseña):
                messages.error(request, 'La contraseña no cumple con los requisitos de seguridad.')
                return render(request, self.template_name, {'form': form, 'validlink': True, 'uid': uidb64, 'token': token})
            
            
            usuario.set_password(nueva_contraseña)  # Método para establecer la nueva contraseña
            usuario.save()
            messages.success(request, 'Tu contraseña ha sido restablecida con éxito.')
            return redirect('login:login')  # Redirigir al inicio de sesión
        else:
            # Si el formulario no es válido, volver a renderizarlo con errores
            messages.error(request, 'Las claves no coinciden.')  
            return render(request, self.template_name, {'form': form, 'validlink': True, 'uid': uidb64, 'token': token})



    def password_meets_criteria(self, password):
        """
        Verifica que la contraseña cumpla con los siguientes criterios:
        1. Al menos un carácter en minúscula.
        2. Al menos un carácter en mayúscula.
        3. Al menos un número.
        4. Al menos un carácter especial.
        5. Al menos 8 caracteres.
        """
        lower = re.compile('(?=.*[a-z])')
        upper = re.compile('(?=.*[A-Z])')
        number = re.compile('(?=.*[0-9])')
        special = re.compile('(?=.*[!@#\\$%\\^&\\*])')
        length = re.compile('(?=.{8,})')

        if (lower.match(password) and
            upper.match(password) and
            number.match(password) and
            special.match(password) and
            length.match(password)):
            return True
        return False







class Usuario_view(LoginRequiredMixin,ListView):
    template_name = 'listado_personal.html'
    model = Usuario
    context_object_name = 'personal'

    
    def get_queryset(self):
        # Filtrar usuarios con is_superuser=False
        return Usuario.objects.filter(is_superuser=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dirurl'] = reverse('login:registro')
        context['title_table'] = 'Listado de Personal'
        context['cancelar'] = reverse('login:personal')
        context['action_save'] = self.request.path
        
        
        return context
