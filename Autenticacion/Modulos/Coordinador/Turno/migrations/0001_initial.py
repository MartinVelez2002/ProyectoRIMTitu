# Generated by Django 5.1.2 on 2024-11-23 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Turno_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('hora_inicio', 'hora_fin'), name='unique_hora_inicio_hora_fin')],
            },
        ),
    ]
