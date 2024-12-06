# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views import generic
from django.views import View
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from pacientes.models import Paciente
from django.db.models import Q

# Modelos
from ..models import Turno
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioTurno

class Listar(LoginRequiredMixin, generic.ListView):
    """
    Lista todos los turnos. 
    """
    model = Turno
    template_name = 'clinica/turnos/lista_turnos.html'
    context_object_name = 'Turnos'
    paginate_by = 5
    # page_kwarg


    def get_queryset(self):
        query = self.request.GET.get('query', None)  
        if query:
            return Turno.objects.filter(
                Q(paciente__nombre__icontains=query) |  
                Q(paciente__documento__icontains=query)  
            ).distinct()
        # Si no hay query, retorna todos los turnos
        return Turno.objects.all()


    def get_context_data(self, **kwargs):

        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Lista de turnos'
        contexto['buscar'] = 'Ingresa el nombre del paciente'
        contexto['url_nuevo'] = reverse_lazy('pacientes:agregar_turno')
        return contexto


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega un nuevo turno y retorna a la lista de turnos.
    """
    model = Turno
    form_class = FormularioTurno
    template_name = 'clinica/turnos/form_turno.html'
    success_url = reverse_lazy('pacientes:lista_turnos')


    def form_valid(self, form):
        try:
            form.instance.clean()
        except ValidationError as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)

        form.instance.asistencia = Turno.ASISTIO_OPCIONES[0][0]  # P - Pendiente
        registrarActividad(self.request, 'Cargó un turno')
        messages.success(self.request, "Turno agendado correctamente.")
        return super().form_valid(form)



    def form_invalid(self, form):
        messages.error(self.request, 'No se pudo agendar el turno. Verifica los datos ingresados.')
        return super().form_invalid(form)
    

  

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Registrar un nuevo turno'
        contexto['volver'] = self.success_url
        return contexto






class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de una determinada observacion

    """
    model = Turno
    form_class = FormularioTurno
    template_name = 'clinica/turnos/form_turno.html'
    success_url = reverse_lazy('pacientes:lista_turnos')

    def form_valid(self, form):
        # Valida si cambiamos el estado del turno
        original_fecha_hora = self.object.fecha_hora
        if 'asistencia' in form.changed_data and len(form.changed_data) == 1:
            messages.success(self.request, "Estado del turno actualizado correctamente.")
            registrarActividad(self.request, 'Modificó un turno')
            return super().form_valid(form)

        # Validar otros cambios (ej. fecha)
        try:
            form.instance.clean()
        except ValidationError as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)

        

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Turno para {self.object.paciente}'
        contexto['url_volver'] = self.success_url
        contexto['editar'] = True
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """
    Elimina un turno.
    """
    model = Turno
    template_name = 'componentes/delete.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó un turno'
        )
        messages.success(
            self.request,
            'Turno eliminado!'
        )
        return reverse_lazy('pacientes:lista_turnos')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar el turno de {self.object.paciente}'
        contexto['url_volver'] = reverse_lazy('pacientes:lista_turnos')
        return contexto

class TurnosCalendarioView(View):
    def get(self, request, *args, **kwargs):
        # Recupera los turnos desde la base de datos
        turnos = Turno.objects.all()

        # Formatea los datos de los turnos para que coincidan con la estructura de eventos de FullCalendar
        eventos = []
        for turno in turnos:
            eventos.append({
                'title': turno.paciente.nombre,  
                'start': turno.fecha_hora.isoformat(),  
                'medico': turno.paciente.medico.nombre,
            })

        return JsonResponse(eventos, safe=False)
