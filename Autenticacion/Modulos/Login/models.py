from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from Modulos.Login.utils import validar_cedula

# Create your models here.



# Modelo de Rol
class Rol(models.Model):
    name = models.CharField(max_length=25, unique=True,  verbose_name="Nombre del rol")
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Roles" 



class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None, cedula=None, rol = None, nombre = None, apellido = None):

        usuario = self.model(
            username=username,
            nombre=nombre,
            apellido=apellido,
            email=self.normalize_email(email),
            password=password,
            cedula = cedula,
            rol=rol
            )

        usuario.set_password(password)
        usuario.is_staff = False  # Establecer a False para usuarios normales
        usuario.is_superuser = False  # Establecer a False para usuarios normales
        usuario.save()
        return usuario

    

    def create_superuser(self, email, username, password=None, cedula=None, rol=None, nombre=None, apellido=None):
        usuario = self.create_user(email,
        username, 
        password
        )
        
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15,unique=True)
    email = models.EmailField(unique=True, max_length=50)
    nombre = models.CharField(max_length = 15, blank = True, null = True)
    apellido = models.CharField(max_length = 15, blank = True, null = True)
    cedula = models.CharField(unique=True, max_length=10 ,validators=[validar_cedula], null=True)
    estado = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Permitir el acceso al admin
    is_superuser = models.BooleanField(default=False)  #Acceso completo y sin restricciones, permitiendo cualquier acción.
    primera_sesion = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, blank=True) 
    
    objects = UsuarioManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
    def save(self, *args, **kwargs):
        # Encripta la contraseña si está en texto plano
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


 



