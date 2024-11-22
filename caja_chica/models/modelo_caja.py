# Python
from datetime import date

# Django
from django.db import models
from django.utils import timezone

# Modelos
from compartido.modelo_base import ModeloBase


class MovimientoCajaChica(models.Model):
    TIPO_MOVIMIENTO = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )

    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    concepto = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.localtime)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "movimiento_caja"
        verbose_name = "Movimiento de Caja Chica"
        verbose_name_plural = "Movimientos de Caja Chica"
        ordering = ['-fecha', '-creado_en']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.monto} - {self.fecha}"


class SaldoDiarioCajaChica(models.Model):
    fecha = models.DateField(unique=True)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_final = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "saldo_diario"
        verbose_name = "Saldo Diario de Caja Chica"
        verbose_name_plural = "Saldos Diarios de Caja Chica"
        ordering = ['-fecha']

    def __str__(self):
        return f"Saldo {self.fecha}: {self.saldo_final}"
    
    def calcular_saldo_final(self):
        entradas = MovimientoCajaChica.objects.filter(tipo='entrada', fecha=self.fecha).aggregate(total=models.Sum('monto'))['total'] or 0
        salidas = MovimientoCajaChica.objects.filter(tipo='salida', fecha=self.fecha).aggregate(total=models.Sum('monto'))['total'] or 0
        self.saldo_final = self.saldo_inicial + entradas - salidas
        self.save()


