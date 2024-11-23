from django.db import models
from Modulos.Coordinador.Calendario.models import TurnUsuario_Model
from Modulos.Coordinador.Novedad.models import Novedad_Model
from django.core.validators import FileExtensionValidator
from Auth.constantes import Opciones
# Create your models here.

class CabIncidente_Model(models.Model):
    agente = models.ForeignKey(TurnUsuario_Model, on_delete=models.PROTECT, related_name='agentes', help_text="Agente responsable del reporte")
    novedad = models.ForeignKey(Novedad_Model, on_delete=models.PROTECT, help_text="Novedad asociada al incidente")
    prioridad = models.CharField(max_length=1, choices=Opciones.prioridad(), help_text="Nivel de prioridad de la incidencia")
    fecha = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación del reporte")   
    
    class Meta:
        verbose_name = "Cabecera de Incidente"
        verbose_name_plural = "Cabeceras de Incidentes"
    
    def __str__(self):
        return f"Reporte {self.id} - {self.get_estado_display()}"

    

class DetIncidente_Model(models.Model):
    cabincidente = models.ForeignKey(CabIncidente_Model, on_delete=models.PROTECT, related_name="detalles", help_text="Referencia a la cabecera del incidente")
    estado_incidente = models.CharField(max_length=1,choices=Opciones.estado_incidente(), default='N', help_text="Estado actualizado de la incidencia")
    hora = models.TimeField(auto_now_add=True,help_text="Fecha y hora de este detalle")
    evidencia = models.FileField(upload_to='media/evidencias',validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'])],blank=True,null=True,help_text="Evidencia adjunta (opcional)")
    descripcion = models.TextField(help_text="Descripción detallada del seguimiento del incidente")
    comentarios_adicionales = models.TextField(blank=True, null=True, help_text="Comentarios adicionales sobre el seguimiento")
 
    
    class Meta:
        verbose_name = "Detalle de Incidente"
        verbose_name_plural = "Detalles de Incidentes"
    
    def __str__(self):
        return f"Detalle {self.id} - Incidente {self.cabincidente.id}"

