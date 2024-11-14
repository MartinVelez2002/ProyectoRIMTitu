from django.db import models

# Create your models here.

class Turno_Model(models.Model):
    hora_inicio = models.TimeField(auto_now = False, auto_now_add= False)
    hora_fin = models.TimeField(auto_now = False, auto_now_add= False)
    estado = models.BooleanField(default = True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hora_inicio', 'hora_fin'], name='unique_hora_inicio_hora_fin')
        ]
        
    def __str__(self):
        return f'{self.hora_inicio} hasta {self.hora_fin}'