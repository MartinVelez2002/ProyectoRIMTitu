from django.db import models

# Create your models here.
class Ubicacion_Model(models.Model):
    Sector = models.CharField(max_length = 100)
    CallePrincipal = models.CharField(max_length = 100)
    Interseccion = models.CharField(max_length = 100)
    Estado = models.BooleanField(default = True)