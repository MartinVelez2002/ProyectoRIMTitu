from django.db import models
from Modulos.Login.models import Usuario 


class Calendario_Model(models.Model):
    Fecha_inicio = models.DateField(auto_now = False)
    Fecha_fin = models.DateField(auto_now = False)
    Estado = models.BooleanField(default = True)

# Create your models here.
class Turno_Model(models.Model):
    Hora_inicio = models.TimeField(auto_now = False, auto_now_add= False)
    Hora_fin = models.TimeField(auto_now = False, auto_now_add= False)
    Estado = models.BooleanField(default = True)

class TurnUsuario_Model(models.Model):
    Usuario = models.ForeignKey(Usuario, on_delete = models.PROTECT)
    Calendario = models.ForeignKey(Calendario_Model, on_delete = models.PROTECT)
    Turno = models.ForeignKey(Turno_Model, on_delete = models.PROTECT)
    Estado = models.BooleanField(default = True)