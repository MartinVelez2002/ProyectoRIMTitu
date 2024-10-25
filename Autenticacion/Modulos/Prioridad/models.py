from django.db import models

# Create your models here.
class Prioridad(models.Model):
    Descripcion = models.CharField(max_length=30)
    Estado = models.BooleanField(default=1)