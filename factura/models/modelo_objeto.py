from datetime import date
from django.db import models
from compartido.modelo_base import ModeloBase


class ObjetoFactura(ModeloBase):
    nombre_objeto = models.CharField(max_length=250, verbose_name="NombreProducto", unique=True)
    codigo_objeto = models.CharField(max_length=250, verbose_name="Codigo Producto", blank=True, null=True)
    precio_objeto = models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name="Precio del producto")
#  todos deben tener los estados para poder hacer la eliminacion logica

    ESTADO_OBJETO_OPCIONES = (
        ('A', 'Activo'),
        ('I', 'Inactivo')
    )

    estado_objeto = models.CharField(
        max_length=1,
        default='A',
        choices=ESTADO_OBJETO_OPCIONES,
        verbose_name="Estado actual del objeto"
        )
    class Meta:
        pass


    def __str__(self):
        return f"{self.codigo_objeto} - {self.nombre_objeto}"

