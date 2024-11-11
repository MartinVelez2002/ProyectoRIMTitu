from django.db import models
from Modulos.Login.models import Usuario 
from Modulos.Coordinador.Ubicacion.models import Ubicacion_Model
from Modulos.Coordinador.Turno.models import Turno_Model


class Calendario_Model(models.Model):
    Fecha_inicio = models.DateField(auto_now = False)
    Fecha_fin = models.DateField(auto_now = False)
    Estado = models.BooleanField(default = True)

class TurnUsuario_Model(models.Model):
    Usuario = models.ForeignKey(Usuario, on_delete = models.PROTECT)
    Calendario = models.ForeignKey(Calendario_Model, on_delete = models.PROTECT)
    Turno = models.ForeignKey(Turno_Model, on_delete = models.PROTECT)
    Ubicacion = models.ForeignKey(Ubicacion_Model, on_delete= models.PROTECT)
    Estado = models.BooleanField(default = True)