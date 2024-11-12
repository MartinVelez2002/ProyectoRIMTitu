from django.db import models

# Create your models here.
class Ubicacion_Model(models.Model):
    Lugar = models.CharField(max_length = 50)
    Sector = models.CharField(max_length = 100)
    CallePrincipal = models.CharField(max_length = 100)
    Estado = models.BooleanField(default = True)
    
    def __str__(self):
        return f'{self.Lugar}'