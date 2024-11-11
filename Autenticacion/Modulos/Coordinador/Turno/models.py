from django.db import models

# Create your models here.

class Turno_Model(models.Model):
    Hora_inicio = models.TimeField(auto_now = False, auto_now_add= False)
    Hora_fin = models.TimeField(auto_now = False, auto_now_add= False)
    Estado = models.BooleanField(default = True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Hora_inicio', 'Hora_fin'], name='unique_hora_inicio_hora_fin')
        ]