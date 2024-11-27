from django.views.generic import ListView
from pacientes.models.modelo_duracion import TiempoAgendamiento
from django.db.models import Avg, Sum








class ReporteTiemposAgendamiento(ListView):
    template_name = 'clinica/reportes/tiempos_agendamiento.html'
    context_object_name = 'tiempos'

    def get_queryset(self):
        return TiempoAgendamiento.objects.all()

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        tiempos = TiempoAgendamiento.objects.all()
        contexto['promedio'] = tiempos.aggregate(Avg('duracion_agendamiento'))['duracion_agendamiento__avg']
        contexto['total'] = tiempos.aggregate(Sum('duracion_agendamiento'))['duracion_agendamiento__sum']
        return contexto



