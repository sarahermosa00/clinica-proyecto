# Django
from django.forms import ModelForm

# Modelos
from .models import *
from usuarios.models import Usuario


class FormularioPaciente(ModelForm):

    class Meta:
        model = Paciente
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].queryset = Usuario.objects.filter(rol='M')

#--------------------------------------
class FormularioObservacion(ModelForm):

    class Meta:
        model = Observacion
        fields = '__all__'

# -------------------------------
class FormularioTurno(ModelForm):

    class Meta:
        model = Turno
        fields = '__all__'