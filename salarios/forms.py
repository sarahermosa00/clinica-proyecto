# Django
from django.forms import ModelForm
from django import forms

# Modelos
from .models import *
from usuarios.models import Usuario

class FormularioCategoria(ModelForm):
    
    class Meta:
        model = Categoria
        fields = '__all__'

#--------------------------------------
class FormularioEmpleado(ModelForm):

    class Meta:
        model = Empleado
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class EstadoWidget(forms.Select):
        def render(self, name, value, attrs=None, renderer=None):
            return super().render(name, value, attrs, renderer)
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        label="Departamento",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'}),
    )

    estado = forms.ChoiceField(
        choices=Empleado.OPCIONES_ESTADO,
        label="Estado",
        widget=EstadoWidget(attrs={'class': 'form-control rounded-pill'}),
    )

#---------------------------------------
class FormularioPagoSalario(forms.ModelForm):
    empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Empleados"
    )

    class Meta:
        model = PagoSalario
        fields = ['empleados']