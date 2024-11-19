from django.db import models
from Modulos.Coordinador.Calendario.models import TurnUsuario_Model
from Modulos.Coordinador.Novedad.models import Novedad_Model
from django.core.validators import FileExtensionValidator
from Auth.constantes import Opciones

# Create your models here.

class CabIncidente_Model(models.Model):
    agente = models.ForeignKey(TurnUsuario_Model, on_delete= models.PROTECT, related_name='agente')
    novedad = models.ForeignKey(Novedad_Model, on_delete = models.PROTECT)
    prioridad = models.CharField(max_length=1, choices=Opciones.prioridad())
    fecha = models.DateField(auto_now= True)
    estado = models.BooleanField(default = True)
    

class DetIncidente_Model(models.Model):
    cabincidente = models.ForeignKey(CabIncidente_Model, on_delete = models.PROTECT)
    estado_incidente = models.CharField(max_length=1, choices = Opciones.estado_incidente(), default='N')
    hora = models.TimeField(auto_now = True)
    evidencia = models.FileField(upload_to='media/evidencias', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'])])
    descripcion = models.CharField(max_length = 300)
    estado = models.BooleanField(default = True)
