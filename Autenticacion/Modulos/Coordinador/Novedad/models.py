from django.db import models
# Create your models here.

class TipoNovedad_Model(models.Model):
    Descripcion = models.CharField(max_length = 50)
    Estado = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.Descripcion}'

class Novedad_Model(models.Model):
    Descripcion = models.CharField(max_length = 50)
    Estado = models.BooleanField(default = True)
    TipoNovedad = models.ForeignKey(TipoNovedad_Model, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.Descripcion}'