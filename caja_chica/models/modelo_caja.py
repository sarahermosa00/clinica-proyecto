# Python
from datetime import date

# Django
from django.db import models
from django.utils import timezone
from decimal import Decimal

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
    cerrado = models.BooleanField(default=False)  # Indica si la caja está cerrada
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Diferencia detectada en el cierre

    class Meta:
        db_table = "saldo_diario_caja"
        verbose_name = "Saldo Diario de Caja Chica"
        verbose_name_plural = "Saldos Diarios de Caja Chica"
        ordering = ['-fecha']

    def calcular_saldo_final(self):
        movimientos = MovimientoCajaChica.objects.filter(fecha=self.fecha)
        entradas = movimientos.filter(tipo='entrada').aggregate(total=models.Sum('monto'))['total'] or 0
        salidas = movimientos.filter(tipo='salida').aggregate(total=models.Sum('monto'))['total'] or 0
        self.saldo_final = self.saldo_inicial + entradas - salidas

        # Actualizar el saldo inicial del día siguiente
        # fecha_siguiente = self.fecha + timezone.timedelta(days=1)
        # saldo_siguiente = SaldoDiarioCajaChica.objects.filter(fecha=fecha_siguiente).first()
        # if saldo_siguiente:
        #     saldo_siguiente.saldo_inicial = self.saldo_final
        #     saldo_siguiente.save()
        if not self.cerrado:
            self._actualizar_saldo_siguiente()
        
        self.save()



    def cerrar_caja(self, saldo_fisico):
        self.cerrado = True
        self.diferencia = Decimal(str(saldo_fisico)) - self.saldo_final  # Calcula la diferencia
        self.saldo_final = Decimal(str(saldo_fisico))  # Ajusta el saldo final con el saldo físico ingresado

        # Actualizar el saldo inicial del día siguiente
        fecha_siguiente = self.fecha + timezone.timedelta(days=1)
        saldo_siguiente, creado = SaldoDiarioCajaChica.objects.get_or_create(fecha=fecha_siguiente)
        saldo_siguiente.saldo_inicial = self.saldo_final
        saldo_siguiente.save()
        # self._actualizar_saldo_siguiente()

        self.save()



    def abrir_caja(self, nuevo_saldo_fisico=None):
        self.cerrado = False
        if nuevo_saldo_fisico is not None:
            from decimal import Decimal
            diferencia = Decimal(str(nuevo_saldo_fisico)) - self.saldo_final
            self.diferencia = diferencia
            self.saldo_final = Decimal(str(nuevo_saldo_fisico))  # Ajusta el saldo final con el nuevo saldo físico

            # Actualizar el saldo inicial del día siguiente
            # fecha_siguiente = self.fecha + timezone.timedelta(days=1)
            # saldo_siguiente = SaldoDiarioCajaChica.objects.filter(fecha=fecha_siguiente).first()
            # if saldo_siguiente:
            #     saldo_siguiente.saldo_inicial = self.saldo_final
            #     saldo_siguiente.save()
            self._actualizar_saldo_siguiente()


        self.save()


    def _actualizar_saldo_siguiente(self):
        """Actualiza el saldo inicial del día siguiente basado en el saldo final del día actual."""
        fecha_siguiente = self.fecha + timezone.timedelta(days=1)
        saldo_siguiente, creado = SaldoDiarioCajaChica.objects.get_or_create(fecha=fecha_siguiente)
        
        # Actualiza el saldo inicial solo si no está cerrado
        if not saldo_siguiente.cerrado:
            saldo_siguiente.saldo_inicial = self.saldo_final
            print("Saldo siguiente es: ", saldo_siguiente.saldo_inicial)
            saldo_siguiente.save()




