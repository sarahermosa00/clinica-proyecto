# Django
from django.db import models
from django.utils import timezone

# Modelos
from compartido.modelo_base import ModeloBase
from . import Paciente
from usuarios.models import Usuario


class Turno(ModeloBase):
    """
    Esta clase contiene la logica para persistir turnos en el sistema.
    El rol de Secretaria/Secretario es el encargado de administrar los pedidos.
    """
    
    ASISTIO_OPCIONES = (
        ('P', 'Pendiente'),
        ('A', 'Asistió'),
        ('F', 'Faltó')
    )

    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        verbose_name="Paciente",
        related_name="turnos"
    ) 

    medico = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        verbose_name="Médico", 
        blank=True,
        null=True
    )

    asistencia = models.CharField(
        max_length=1, 
        choices=ASISTIO_OPCIONES,  
        verbose_name="Asistencia",
        blank=True,
        null=True
    )
    
    # se quiere poner la hora tambien para evitar poner dos turnos en el mismo horario

    fecha_hora = models.DateTimeField(verbose_name="Fecha y hora", default=timezone.now)

    class Meta:
        db_table = "turno"
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"




    
    def __str__(self):
        return f"{self.paciente.nombre} {self.paciente.apellido}, {self.fecha_hora}"




