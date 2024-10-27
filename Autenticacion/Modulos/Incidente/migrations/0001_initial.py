# Generated by Django 5.1.2 on 2024-10-27 02:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Novedad', '0001_initial'),
        ('Prioridad', '0003_rename_prioridad_prioridad_model'),
        ('Ubicacion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoIncidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Descripcion', models.CharField(max_length=20)),
                ('Estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CabIncidente_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateField()),
                ('Estado', models.BooleanField(default=True)),
                ('Agente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agente', to=settings.AUTH_USER_MODEL)),
                ('Lugar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Ubicacion.ubicacion_model')),
                ('Novedad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Novedad.novedad_model')),
                ('Prioridad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Prioridad.prioridad_model')),
                ('Supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supervisor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
