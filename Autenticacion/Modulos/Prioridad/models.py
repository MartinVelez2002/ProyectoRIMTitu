from django.db import models

# Create your models here.
class Prioridad_Model(models.Model):
    Descripcion = models.CharField(max_length=30)
    Estado = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.Descripcion}'