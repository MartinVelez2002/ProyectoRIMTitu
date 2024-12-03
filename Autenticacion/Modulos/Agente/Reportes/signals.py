from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from Modulos.Login.models import Usuario
from .models import CabIncidente_Model

@receiver(post_save, sender=CabIncidente_Model)
def enviar_notificacion_al_crear_reporte(sender, instance, created, **kwargs):
    if created:
        # Obtener a todos los coordinadores activos
        coordinadores = Usuario.objects.filter(rol__name='Coordinador', estado=True)

        if coordinadores.exists():
            # Obtener los correos electrónicos de los coordinadores
            destinatarios = coordinadores.values_list('email', flat=True)

            # Obtener los datos necesarios para el correo
            novedad = instance.novedad 
            prioridad = instance.get_prioridad_display()
            fecha = instance.fecha
            agente = instance.agente.usuario.nombre  

            # Renderizar el mensaje en HTML
            subject = f'Nuevo Reporte de Incidencia Creado: {instance.id}'
            email_template_name = "notificacion_reporte.html"
            context = {
                'novedad': novedad,
                'prioridad': prioridad,
                'fecha': fecha,
                'agente': agente,
            }

            html_message = render_to_string(email_template_name, context)

            from_email = settings.DEFAULT_FROM_EMAIL

            # Enviar el correo a todos los coordinadores
            send_mail(
                subject,
                '',  # Dejar vacío el mensaje de texto plano si solo envías HTML
                from_email,
                destinatarios,  # Lista de correos
                fail_silently=False,
                html_message=html_message)