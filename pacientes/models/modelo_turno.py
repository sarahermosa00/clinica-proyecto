# Django
from django.db import models
from django.utils import timezone

# Modelos
from compartido.modelo_base import ModeloBase
from . import Paciente
from usuarios.models import Usuario

from django.core.exceptions import ValidationError


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


    def clean(self):
        # Validacion para que no se pueda crear turnos pasados a la fecha actual, pero esto solo afecta a la creacion ya que si va editar el estado no afecta.
        if self.fecha_hora < timezone.localtime() and not self.pk:
            raise ValidationError("No se puede agendar un turno en una fecha y hora pasada.")
        
        # Preguntamos si el objeto ya existe en la base de datos
        if self.pk:
            try:
                original = Turno.objects.get(pk=self.pk)
                if original.fecha_hora != self.fecha_hora and self.fecha_hora < timezone.localtime():
                    raise ValidationError("No se puede modificar un turno a una fecha y hora pasada.")
            except Turno.DoesNotExist:
                # Si por alguna razón no se encuentra el objeto, ignorar esta validación
                pass

        super().clean()

        
    def __str__(self):
        return f"{self.paciente.nombre} {self.paciente.apellido}, {self.fecha_hora}"




