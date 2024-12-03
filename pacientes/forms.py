# Django
from django.forms import ModelForm
from django import forms

# Modelos
from .models import *
from usuarios.models import Usuario

# para medir el tiempo de agendamiento de paciente y de turno
from django.utils.timezone import now, localtime
from datetime import timedelta
from django.utils import timezone
from pacientes.models.modelo_duracion import TiempoAgendamiento
#-------------------------------------- 

from django.core.exceptions import ValidationError



class FormularioPaciente(ModelForm):
    

    class Meta:
        model = Paciente
        fields = '__all__'

    class GeneroWidget(forms.Select):
        def render(self, name, value, attrs=None, renderer=None):
            return super().render(name, value, attrs, renderer)
    
    medico = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(rol='M'),
        label="Médico",
        empty_label="Selecciona un medico",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'}),
        to_field_name='id',
    )

    genero = forms.ChoiceField(
        choices=Paciente.GENERO_CHOICES,
        label="Género",
        widget=GeneroWidget(attrs={'class': 'form-control rounded-pill'}),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].widget.choices = [(user.id, f"{user.nombre.upper()} {user.apellido.upper()}") for user in Usuario.objects.filter(rol='M')]

    #  se sobreescribe el metodo save para preguntar cuanto tiempo tomo ejecutar este formulario desde su inicio hasta su final para poder medir cuanto toma registrar un paciente usando el sistema

    def save(self, commit=True):
        inicio_medicion_paciente =  now()
        instancia = super().save(commit=commit)
        final_medicion_paciente = now()

        duracion_turno_paciente = (final_medicion_paciente -inicio_medicion_paciente).total_seconds()
        print(f"El tiempo de ejecución de la carga de paciente fue de {duracion_turno_paciente} segundos") 
        return instancia   
    



#--------------------------------------
class FormularioObservacion(ModelForm):

    class Meta:
        model = Observacion
        fields = '__all__'

    class GeneroWidget(forms.Select):
        def render(self, name, value, attrs=None, renderer=None):
            return super().render(name, value, attrs, renderer)

    especialidad = forms.ChoiceField(
        choices=Observacion.especialidad_choices,
        label="Especialidad",
        widget=GeneroWidget(attrs={'class': 'form-control rounded-pill'}),
    )

# -------------------------------
class FormularioTurno(ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'

# Este widget sirve para que despues el javascript no tenga problemas para usar flatpickr

        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'type': 'datetime-local'
            }),
        }

    medico = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(rol='M'),
        label="Médico",
        empty_label="Selecciona un medico",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'}),
        to_field_name='id',
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_hora = cleaned_data.get('fecha_hora')
        medico = cleaned_data.get('medico')


        # para que no se pueda poner una cita hacia el pasado
        if fecha_hora and fecha_hora < timezone.now():
            raise ValidationError("No se puede agendar un turno en una fecha y hora pasada.")

        # para que no se pueda poner dos turnos en el mismo horario
        rango_tiempo = timedelta(minutes=45)
        conflictos = Turno.objects.filter(
            medico=medico,
            fecha_hora__range=(fecha_hora - rango_tiempo, fecha_hora + rango_tiempo)
        )
        if conflictos.exists():
            raise ValidationError("Ya existe un turno agendado para el médico en un rango de 45 minutos.")

        return cleaned_data
    

# ----------------------Mediciones----------------------

    # Esta parte sobreescribimos el metodo save para recoger datos de cuanto tiempo dura agendar un turno para comparar con el proceso que se seguia manualmente antes de implementar el sistema
    def save(self, commit=True):

        inicio_medicion_turno = now()
        instancia = super().save(commit=commit)
        final_medicion_turno = now()

        duracion_turno = (final_medicion_turno - inicio_medicion_turno).total_seconds()

        try:
            TiempoAgendamiento.objects.create(
                fecha_agendamiento=final_medicion_turno,
                duracion_agendamiento=duracion_turno,
                turno=instancia,
            )
        except Exception as e:
            print(f"Error al guardar el tiempo de agendamiento: {e}")

        return instancia

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].widget.choices = [
            (user.id, f"{user.nombre.upper()} {user.apellido.upper()}")
            for user in Usuario.objects.filter(rol='M')
        ]
