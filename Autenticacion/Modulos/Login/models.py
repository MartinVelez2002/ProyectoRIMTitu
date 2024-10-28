from django.db import models
from Auth.constantes import Opciones
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


ROL = Opciones.rol()
PERMISOS_COORDINADOR, PERMISOS_AGENTE_CONTROL = Opciones.permiso()



class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        usuario = self.model(
            username=username,
            email=self.normalize_email(email),
            )

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, username, password):
        usuario = self.create_user(
            email,
            username=username,
            password=password
        )

        usuario.usuario_administrador = True
        usuario.save()
        return usuario



class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=20,unique=True)
    email = models.EmailField(unique=True, max_length=50)
    nombre = models.CharField(max_length = 20, blank = True, null = True)
    apellido = models.CharField(max_length = 20, blank = True, null = True)
    cedula = models.CharField(unique=True, max_length=10 ,validators=[RegexValidator(regex='^.{10}$', message='Introduzca una cédula válida')], default='')
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    rol = models.CharField(max_length=10, choices=ROL,default=ROL[0][1], blank=True, null=True)
    
    
    objects = UsuarioManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


    
    
    def get_permisos(self):
    # Devuelve los permisos según el rol asignado: Coordinador si es administrador, Agente de Control si no lo es
        if self.usuario_administrador:
            return PERMISOS_COORDINADOR
        elif self.rol == 'AC':
            return PERMISOS_AGENTE_CONTROL
        return set()

    def has_perm(self, perm, obj=None):
        # Comprueba si el usuario tiene un permiso específico
        return perm in self.get_permisos()

    def has_module_perms(self, app_label):
        # Permite acceso a los módulos de la app
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador
    
    

    
    
    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True


