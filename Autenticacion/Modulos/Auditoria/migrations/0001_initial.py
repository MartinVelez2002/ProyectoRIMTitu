# Generated by Django 5.1.2 on 2024-11-11 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditoriaUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(choices=[('M', 'Modificar'), ('C', 'Crear'), ('E', 'Eliminar')], max_length=1, verbose_name='Acción')),
                ('tabla', models.CharField(max_length=100, verbose_name='Tabla')),
                ('registro_id', models.IntegerField(verbose_name='ID de Registro')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha y Hora')),
                ('hora', models.TimeField(auto_now_add=True, verbose_name='Hora')),
                ('nombre_maquina', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de la Máquina')),
                ('estacion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Estación')),
            ],
            options={
                'verbose_name': 'Auditoría de Usuario',
                'verbose_name_plural': 'Auditorías de Usuarios',
                'ordering': ('-fecha',),
            },
        ),
    ]
