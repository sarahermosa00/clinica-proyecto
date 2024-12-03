from django.db import models
from django.utils.timezone import now
from pacientes.models.modelo_turno import Turno





class TiempoAgendamiento(models.Model):
    fecha_agendamiento = models.DateTimeField(default=now, verbose_name="Fecha de agendamiento")    
    duracion_agendamiento = models.FloatField(verbose_name="Duración de agendamiento")  
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, verbose_name="Turno ")


    def __str__(self):  
        return f"{self.fecha_agendamiento} - {self.duracion_agendamiento}"  
    


