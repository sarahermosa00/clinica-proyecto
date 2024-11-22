from datetime import date
from django.db import models
from compartido.modelo_base import ModeloBase
"""from factura.views.proveedores import Proveedor"""


class Proveedor(models.Model):
    """
    Datos que necesito en mi proveedor
    ------------------------------------

    razon social descripcion

    ruc

    telefono

    direccion

    tipo cliente proveedor ambos

    estado
    """
    razon_social = models.CharField(max_length=250, verbose_name="Razon social")
    ruc = models.CharField(max_length=9, verbose_name="RUC")
    telefono = models.CharField(max_length=12, verbose_name="Telefono o celular")
    direccion = models.CharField(max_length=250, verbose_name="Direccion")
    TIPO_CLIENTE_OPCIONES = [
        ('C', 'Cliente'),
        ('P', 'Proveedor'),
        ('A', 'Ambos')
    ]

    tipo = models.CharField(
        max_length=1,
        choices=TIPO_CLIENTE_OPCIONES,
        default='C',
        verbose_name="Tipo de entidad (Cliente, Proveedor, Ambos)"
    )

    ESTADO_OPCIONES = (
        ('A', 'Activo'),
        ('I', 'Inactivo')
    )

    estado = models.CharField(
        max_length=1,
        default='A',
        choices=ESTADO_OPCIONES,
        verbose_name="Estado actual de la factura"
    )

    class Meta:
        pass

        """Para luego definir permisos, etc"""


    def __str__(self):
        return f"{self.razon_social} - {self.ruc}"
    
    """el display obtiene los valores que estan por defecto """
    



