from django.db import models
# Create your models here.

class TipoNovedad_Model(models.Model):
    descripcion = models.CharField(unique= True, max_length = 50)
    estado = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.descripcion}'

class Novedad_Model(models.Model):
    descripcion = models.CharField(unique= True, max_length = 50)
    estado = models.BooleanField(default = True)
    tiponovedad = models.ForeignKey(TipoNovedad_Model, on_delete=models.PROTECT)
    
    class Meta:
        unique_together = ('descripcion', 'tiponovedad')
        
    def __str__(self):
        return f'{self.descripcion}'
    