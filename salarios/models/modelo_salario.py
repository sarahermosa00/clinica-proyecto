# Python
from datetime import date

# Django
from django.db import models

# Modelos
from compartido.modelo_base import ModeloBase


class Categoria(models.Model):
    """ 
    Representa la categoría de empleados, como un rol o área específica.
    """
    nombre = models.CharField(max_length=250, verbose_name="Nombre de la categoría")

    class Meta:
        db_table = "categoria"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


class Empleado(ModeloBase):
    """ 
    Representa a un empleado dentro de la organizacion.
    """
    nombre = models.CharField(max_length=500, verbose_name="Nombre")
    documento = models.CharField(max_length=11, unique=True, verbose_name="documento")
    cuenta_bancaria = models.CharField(max_length=30, verbose_name="Cuenta Bancaria", blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria", blank=True, null=True)
    salario_base = models.DecimalField(max_digits=14, decimal_places=2, default=0.0, verbose_name="Salario base")
    bonificaciones = models.DecimalField(max_digits=14, decimal_places=2, default=0.0, verbose_name="Total de bonificaciones")
    deducciones = models.DecimalField(max_digits=14, decimal_places=2, default=0.0, verbose_name="Total de deducciones")
    fecha_contratacion = models.DateField(verbose_name="Fecha de contratación")
    fecha_terminacion = models.DateField(blank=True, null=True, verbose_name="Fecha de terminación")
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Número de teléfono")

    OPCIONES_ESTADO = (
    ('A', 'Activo'),
    ('I', 'Inactivo'),
    )

    estado = models.CharField(
        max_length=1,
        default='A',
        choices=OPCIONES_ESTADO,
        verbose_name="Estado actual del empleado"
    )

    class Meta:
        db_table = "empleado"
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['created_at']


    def __str__(self):
        return f"{self.nombre} | Categoría: {self.categoria.nombre}"


class PagoSalario(ModeloBase):
    """ 
    Gestiona los pagos de salarios de los empleados, teniendo en cuenta bonificaciones y deducciones.
    Un solo registro de pago puede involucrar varios empleados.
    """
    empleados = models.ManyToManyField('Empleado', verbose_name="Empleados")
    fecha_pago = models.DateField(verbose_name="Fecha de pago")
    salario_total = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Salario total", editable=False)

    def calcular_salario(self):
        """ 
        Calcula el salario total basado en la suma de salarios, bonificaciones y deducciones de los empleados seleccionados.
        """
        salario_total = 0
        for empleado in self.empleados.all():
            salario_base = empleado.salario_base
            bonificaciones = empleado.bonificaciones
            deducciones = empleado.deducciones

            # Calcula el salario del empleado
            salario_empleado = salario_base + bonificaciones - deducciones
            salario_total += salario_empleado

        # Actualiza el salario total del pago
        self.salario_total = salario_total
        self.save()

    class Meta:
        verbose_name = "salario"
        verbose_name_plural = "salarios"
        db_table = "salario"
        ordering = ['created_at']


    def __str__(self):
        return f"Pago del {self.fecha_pago}"