# Django
from django.forms import ModelForm
from django import forms

# Modelos
from .models import *
from usuarios.models import Usuario


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

    medico = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(rol='M'),
        label="Médico",
        empty_label="Selecciona un medico",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'}),
        to_field_name='id',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].widget.choices = [(user.id, f"{user.nombre.upper()} {user.apellido.upper()}") for user in Usuario.objects.filter(rol='M')]
