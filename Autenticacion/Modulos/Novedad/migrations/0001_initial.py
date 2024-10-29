# Generated by Django 5.1.2 on 2024-10-29 13:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoNovedad_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Descripcion', models.CharField(max_length=30)),
                ('Estado', models.BooleanField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Novedad_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Descripcion', models.CharField(max_length=30)),
                ('Estado', models.BooleanField(default=True)),
                ('TipoNovedad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Novedad.tiponovedad_model')),
            ],
        ),
    ]
