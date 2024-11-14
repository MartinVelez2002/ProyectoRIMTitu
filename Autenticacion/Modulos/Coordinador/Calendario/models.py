from django.db import models
from Modulos.Login.models import Usuario 
from Modulos.Coordinador.Ubicacion.models import Ubicacion_Model
from Modulos.Coordinador.Turno.models import Turno_Model


class Calendario_Model(models.Model):
    fecha_inicio = models.DateField(auto_now = False)
    fecha_fin = models.DateField(auto_now = False)
    estado = models.BooleanField(default = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fecha_inicio', 'fecha_fin'], name = 'fecha_unica')
        ]
    def __str__(self):
        return f'{self.fecha_inicio} hasta {self.fecha_fin}'

class TurnUsuario_Model(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete = models.PROTECT)
    calendario = models.ForeignKey(Calendario_Model, on_delete = models.PROTECT)
    turno = models.ForeignKey(Turno_Model, on_delete = models.PROTECT)
    ubicacion = models.ForeignKey(Ubicacion_Model, on_delete= models.PROTECT)
    estado = models.BooleanField(default = True)
    
    def get_queryset(self):
        # Filtrar el queryset de TurnUsuario_Model, incluyendo solo los registros donde el usuario no es superusuario
        return TurnUsuario_Model.objects.filter(usuario__is_superuser=False)
    