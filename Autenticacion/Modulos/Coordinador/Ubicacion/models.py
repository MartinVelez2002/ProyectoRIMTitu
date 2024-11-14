from django.db import models

# Create your models here.
class Ubicacion_Model(models.Model):
    lugar = models.CharField(max_length = 50)
    sector = models.CharField(max_length = 100)
    calleprincipal = models.CharField(max_length = 100)
    estado = models.BooleanField(default = True)
    
    def __str__(self):
        return f'{self.lugar}'