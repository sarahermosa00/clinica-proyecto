# Django
from django.forms import ModelForm
from django import forms

# Modelos
from .models import *
from usuarios.models import Usuario

from .models import MovimientoCajaChica, SaldoDiarioCajaChica

class MovimientoCajaChicaForm(forms.ModelForm):
    class Meta:
        model = MovimientoCajaChica
        fields = ['tipo', 'concepto', 'monto', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

#---------------------------------------

class SaldoDiarioCajaChicaForm(forms.ModelForm):
    class Meta:
        model = SaldoDiarioCajaChica
        fields = ['fecha', 'saldo_inicial']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'saldo_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
        }
#---------------------------------------
