from django.db import models
from Modulos.Login.models import Usuario

class AuditoriaUser(models.Model):
    class AccionChoices(models.TextChoices):
        MODIFICAR = 'M', 'Modificar'
        CREAR = 'C', 'Crear'
        ELIMINAR = 'E', 'Eliminar'

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        verbose_name='Usuario'
    )
    accion = models.CharField(
        max_length=1,
        choices=AccionChoices.choices,
        verbose_name='Acción'
    )
    tabla = models.CharField(max_length=100, verbose_name='Tabla')
    registro_id = models.IntegerField(verbose_name='ID de Registro')
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha y Hora')
    hora = models.TimeField(auto_now_add=True, verbose_name='Hora')
    nombre_maquina = models.CharField(max_length=100, verbose_name='Nombre de la Máquina', null=True, blank=True)
    estacion = models.CharField(max_length=100, verbose_name='Estación', null=True, blank=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.tabla} - {self.get_accion_display()} ({self.fecha})"


    class Meta:
        verbose_name = 'Auditoría de Usuario'
        verbose_name_plural = 'Auditorías de Usuarios'
        ordering = ('-fecha',)

    
    
    
    
    
    
    
    
    
