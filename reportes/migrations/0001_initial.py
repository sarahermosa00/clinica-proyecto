# Generated by Django 4.2.5 on 2023-09-14 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filtro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filtro', models.CharField(max_length=200, verbose_name='Filtro')),
                ('recurso', models.CharField(max_length=200, verbose_name='Recurso')),
            ],
        ),
    ]
