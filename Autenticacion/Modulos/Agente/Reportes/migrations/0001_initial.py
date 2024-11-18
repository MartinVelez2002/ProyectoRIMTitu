# Generated by Django 5.1.2 on 2024-11-15 01:52

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Novedad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reportes_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
                ('prioridad', models.CharField(choices=[('A', 'Alto'), ('M', 'Medio'), ('B', 'Bajo')], max_length=1)),
                ('evidencia', models.FileField(upload_to='media/evidencias', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'])])),
                ('estado_incidente', models.CharField(choices=[('R', 'Resuelto'), ('E', 'En Proceso'), ('N', 'Notificado')], default='N', max_length=1)),
                ('hora', models.TimeField(auto_now=True)),
                ('descripcion', models.CharField(max_length=300)),
                ('novedad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Novedad.novedad_model')),
            ],
        ),
    ]