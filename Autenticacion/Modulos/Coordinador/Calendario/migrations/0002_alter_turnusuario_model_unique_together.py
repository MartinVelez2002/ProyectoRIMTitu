# Generated by Django 5.1.2 on 2024-11-26 16:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Calendario', '0001_initial'),
        ('Turno', '0001_initial'),
        ('Ubicacion', '0002_alter_ubicacion_model_lugar'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='turnusuario_model',
            unique_together={('usuario', 'calendario', 'turno', 'ubicacion')},
        ),
    ]
