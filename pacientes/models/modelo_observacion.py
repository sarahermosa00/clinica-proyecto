# Django
from django.db import models

# Modelos
from compartido.modelo_base import ModeloBase
from .modelo_paciente import Paciente

class Observacion(ModeloBase):
    """
    Solo un Profesional médico debe agregar registros al historial de cada paciente.
    El conjunto de registros de cada paciente crea su historial médico.
    """
    motivo_consulta = models.CharField(max_length=100, verbose_name="Motivo")
    especialidad_choices = (
        ('Fisioterapia', 'Fisioterapia'),
        ('Psicologia', 'Psicologia'),
        ('Ginecologia', 'Ginecologia'),

    )
    especialidad = models.CharField(
        verbose_name="Especialidad",
        max_length=50, 
        blank=True,
        choices=especialidad_choices,
        default='Fisioterapia',
        help_text="Nombre de la especialidad donde el/la paciente consulta"
    )
    tratamientos = models.TextField(verbose_name="Tratamiento", max_length=200, blank=True, null=True, help_text="Prescripciones médicas farmacológicas y no farmacológicas ")
    procedimientos = models.TextField(verbose_name="Procedimiento", max_length=200, blank=True, null=True, help_text="Tipo de procedimiento o actividad que se realizó en la consulta")

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente", related_name="observaciones", blank=True, null=True)

    class Meta:
        db_table = 'observacion'
        verbose_name = 'Observación'
        verbose_name_plural = 'Observaciones'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.paciente}, {self.motivo_consulta}"