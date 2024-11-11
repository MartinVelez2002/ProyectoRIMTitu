# Generated by Django 5.1.2 on 2024-11-11 17:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Incidente', '0001_initial'),
        ('Novedad', '0001_initial'),
        ('Ubicacion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cabincidente_model',
            name='Agente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cabincidente_model',
            name='Lugar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Ubicacion.ubicacion_model'),
        ),
        migrations.AddField(
            model_name='cabincidente_model',
            name='Novedad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Novedad.novedad_model'),
        ),
        migrations.AddField(
            model_name='cabincidente_model',
            name='Supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supervisor', to=settings.AUTH_USER_MODEL),
        ),
    ]
