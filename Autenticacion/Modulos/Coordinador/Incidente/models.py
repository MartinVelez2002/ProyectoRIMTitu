from django.db import models
from Modulos.Coordinador.Ubicacion.models import Ubicacion_Model
from Modulos.Login.models import Usuario
from Modulos.Coordinador.Novedad.models import Novedad_Model

# Create your models here.
class CabIncidente_Model(models.Model):
    lugar = models.ForeignKey(Ubicacion_Model, on_delete = models.PROTECT)
    agente = models.ForeignKey(Usuario, on_delete = models.PROTECT, name = 'Agente', related_name = 'agente')
    novedad = models.ForeignKey(Novedad_Model, on_delete = models.PROTECT)
    fecha = models.DateField(auto_now = False)
    estado = models.BooleanField(default = True)
    

# class DetIncidente_Model(models.Model):
#     cabincidente = models.ForeignKey(cabincidente_Model, on_delete = models.PROTECT)
#     estadoIncidente = models.ForeignKey(estadoincidente, on_delete = models.PROTECT)
#     hora = models.TimeField(auto_now = True)
#     evidencia = models.FileField()
#     descripcion = models.CharField(max_length = 300)
#     estado = models.BooleanField(default = True)