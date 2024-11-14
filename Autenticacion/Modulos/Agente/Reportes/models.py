from django.db import models
from Auth.constantes import Opciones
from django.core.validators import FileExtensionValidator
from Modulos.Coordinador.Novedad.models import Novedad_Model

# Create your models here.

class Reportes_Model(models.Model):
    fecha = models.DateField(auto_now = True)

    prioridad = models.CharField(max_length=1, 
    choices=Opciones.prioridad())
    
    novedad = models.ForeignKey(Novedad_Model, on_delete=models.PROTECT)
    
    evidencia = models.FileField(upload_to='media/evidencias', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'])])
    
    estado_incidente = models.CharField(max_length=1, choices = Opciones.estado_incidente(), default='N')
    
    hora = models.TimeField(auto_now = True)
    
    descripcion = models.CharField(max_length = 300)

