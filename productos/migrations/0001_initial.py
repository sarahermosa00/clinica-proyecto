# Generated by Django 4.2.5 on 2023-09-14 22:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, verbose_name='Nombre de la categoria')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('cantidad', models.PositiveIntegerField(default=1, verbose_name='Cantidad')),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=14, verbose_name='Total del detalle')),
            ],
            options={
                'verbose_name': 'Detalle del pedido',
                'verbose_name_plural': 'Detalles de pedidos',
                'db_table': 'detalle_pedido',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('nombre', models.CharField(max_length=250, unique=True, verbose_name='Nombre')),
                ('cod_producto', models.CharField(blank=True, max_length=100, null=True, verbose_name='Código del producto')),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='Precio')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos/img/', verbose_name='Imagen del producto')),
                ('stock', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Cantidad')),
                ('armazon', models.BooleanField(default=False, verbose_name='Armazon')),
                ('lente', models.BooleanField(default=False, verbose_name='Es un lente')),
                ('lado', models.CharField(blank=True, choices=[('izquierdo', 'Izquierdo'), ('derecho', 'Derecho')], default='izquierdo', max_length=9, null=True, verbose_name='Para que ojo')),
                ('distancia', models.CharField(blank=True, choices=[('lejos', 'Lejos'), ('cerca', 'Cerca')], default='lejos', max_length=5, null=True, verbose_name='Distancia')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='productos.categoria', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'producto',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('T', 'Taller'), ('F', 'Finalizado')], default='P', max_length=1, verbose_name='Estado actual del pedido')),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=14, null=True, verbose_name='Sub-total')),
                ('tipo_de_pago', models.CharField(choices=[('TC', 'Tarjeta de credito'), ('BV', 'Billetera virtual'), ('EF', 'Efectivo'), ('DE', 'Debito')], default='TC', max_length=2, verbose_name='Tipo de pago')),
                ('fecha_venta', models.DateField(blank=True, null=True, verbose_name='Fecha')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.paciente', verbose_name='Paciente')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'pedido',
                'ordering': ['created_at'],
            },
        ),
    ]
