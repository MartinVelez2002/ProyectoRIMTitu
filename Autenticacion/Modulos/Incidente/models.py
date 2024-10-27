from django.db import models
from Modulos.Ubicacion.models import Ubicacion_Model
from Modulos.Login.models import Usuario
from Modulos.Novedad.models import Novedad_Model
from Modulos.Prioridad.models import Prioridad_Model
# Create your models here.
class CabIncidente_Model(models.Model):
    Lugar = models.ForeignKey(Ubicacion_Model, on_delete = models.PROTECT)
    Agente = models.ForeignKey(Usuario, on_delete = models.PROTECT, name = 'Agente', related_name = 'agente')
    Supervisor = models.ForeignKey(Usuario, on_delete = models.PROTECT, name = 'Supervisor', related_name = 'supervisor')
    Novedad = models.ForeignKey(Novedad_Model, on_delete = models.PROTECT)
    Prioridad = models.ForeignKey(Prioridad_Model, on_delete = models.PROTECT)
    Fecha = models.DateField(auto_now = False)
    Estado = models.BooleanField(default = True)
    

# class DetIncidente_Model(models.Model):
#     CabIncidente = models.ForeignKey(CabIncidente_Model, on_delete = models.PROTECT)
#     EstadoIncidente = models.ForeignKey(EstadoIncidente, on_delete = models.PROTECT)
#     Hora = models.TimeField(auto_now = True)
#     Evidencia = models.FileField()
#     Descripcion = models.CharField(max_length = 300)
#     Estado = models.BooleanField(default = True)