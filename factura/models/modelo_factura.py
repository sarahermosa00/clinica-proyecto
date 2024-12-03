from datetime import date
from django.db import models
from compartido.modelo_base import ModeloBase
from factura.models.modelo_proveedor import Proveedor
from factura.models.modelo_objeto import ObjetoFactura
from datetime import datetime
from django.core.exceptions import ValidationError



class Factura(ModeloBase):

    # para que se añada automaticamente la fecha de ahora mismo 
    fecha_emision = models.DateTimeField(auto_now_add=True) 
    # importo desde la clase de Proveedor del otro modelo para luego cuando le de a seleccionar se abra un select 2 con los proveedores
    cliente_proveedor = models.ForeignKey(Proveedor, on_delete=models.RESTRICT)
    timbrado = models.CharField(max_length=20, verbose_name = 'Timbrado', default='123456789')     
    inicio_validez_timbrado = models.DateField(default=datetime(2023, 12, 12)) 
    fin_validez_timbrado = models.DateField(default=datetime(2025, 10, 23)) 
    # paara poner una fecha establecida

    ESTADO_FACTURA_OPCIONES = (
        ('V', 'Vigente'),
        ('C', 'Cancelada'),
        ('A', 'Anulada'),
        ('P', 'Pendiente'),
        ('R', 'Rechazada')

    )

    estado_factura_opciones = models.CharField(
        max_length=1,
        choices=ESTADO_FACTURA_OPCIONES,
        default='P',
        verbose_name="Estado actual de la factura : Vigente, Cancelada, Anulada, Pendiente, Rechazada"  
    )

    class Meta:
        pass


    def clean(self):
        if self.fin_validez_timbrado < self.inicio_validez_timbrado:
            raise ValidationError("La fecha de fin de validez no puede ser anterior a la fecha de inicio.")

    def __str__(self):
        return f"{self.fecha_emision} - {self.timbrado}"


# -------En esta parte se define la tabla intermedia para unir objetos con facturas


class DetalleFactura(ModeloBase):
    factura = models.ForeignKey(Factura, on_delete=models.RESTRICT, default=1)
    objeto = models.ForeignKey(ObjetoFactura, on_delete=models.RESTRICT, default=1)
    precio = models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name="Precio del producto")
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        pass

    def __str__(self):
        return f"{self.precio} - {self.cantidad}"
    



