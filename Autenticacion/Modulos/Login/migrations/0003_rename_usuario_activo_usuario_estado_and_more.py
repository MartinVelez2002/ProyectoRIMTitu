# Generated by Django 5.1.2 on 2024-10-29 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_remove_usuario_apellidos_remove_usuario_nombres_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario_activo',
            new_name='estado',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(blank=True, choices=[('S', 'Supervisor'), ('AC', 'Agente de Control')], default='Supervisor', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
