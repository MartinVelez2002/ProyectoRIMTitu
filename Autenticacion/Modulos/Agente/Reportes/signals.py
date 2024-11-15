from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reportes_Model
from Modulos.Coordinador.Incidente.models import CabIncidente_Model, DetIncidente_Model
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Reportes_Model)
def crear_o_actualizar_incidente_automatico(sender, instance, created, **kwargs):
    # Si es un nuevo reporte, crea los objetos asociados
    if created:
        cab_incidente = CabIncidente_Model.objects.create(
            lugar=instance.lugar,
            agente=instance.agente,
            novedad=instance.novedad,
            fecha=instance,
            estado=True
        )
        DetIncidente_Model.objects.create(
            cabincidente=cab_incidente,
            estadoIncidente=cab_incidente,
            hora=instance.hora,
            evidencia=instance.evidencia,
            descripcion=instance.descripcion,
            estado=True
        )
    # Si es una actualización de un reporte existente
    else:
        # Actualiza el objeto existente relacionado
        cab_incidente = CabIncidente_Model.objects.get(fecha=instance)
        cab_incidente.lugar = instance.lugar
        cab_incidente.agente = instance.agente
        cab_incidente.novedad = instance.novedad
        cab_incidente.estado = instance.estado
        cab_incidente.save()

        det_incidente = DetIncidente_Model.objects.get(cabincidente=cab_incidente)
        det_incidente.hora = instance.hora
        det_incidente.evidencia = instance.evidencia
        det_incidente.descripcion = instance.descripcion
        det_incidente.estado = instance.estado
        det_incidente.save()

