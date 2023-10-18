# Generated by Django 4.2.5 on 2023-10-17 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0007_alter_observacion_especialidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='especialidad',
            field=models.CharField(blank=True, choices=[('Fisioterapia', 'Fisioterapia'), ('Psicologia', 'Psicologia'), ('Ginecologia', 'Ginecologia')], default='Fisioterapia', help_text='Nombre de la especialidad donde el/la paciente consulta', verbose_name='Especialidad'),
        ),
    ]
