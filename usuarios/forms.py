# Django
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

# Modelos
from .models import Usuario

class FormularioUsuario(UserCreationForm):

    class Meta:
        model = Usuario
        fields = (
            'username', 'password1', 'password2', 'rol', 'nombre', 'apellido', 'imagen', 'email', 'documento'
            )
    #para filtrar en el form de crear usuario solo los roles creados hasta el release 3    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones del campo 'rol' para mostrar solo 'Medico' y 'Secretaria'
        self.fields['rol'].queryset = Usuario._meta.get_field('rol').choices  # Filtra solo las opciones predefinidas
        self.fields['rol'].choices = [choice for choice in Usuario._meta.get_field('rol').choices if choice[0] in ['S', 'M', 'A', 'G']]

    # Validación personalizada para el campo email
    def clean_email(self):
        email = self.cleaned_data.get('email')
         # Permite gmail, hotmail y dominios propios
        valid_domains = [r'@gmail\.com$', r'@hotmail\.com$', r'@fundacion\.com$'] 

        # Verifica si el correo coincide con alguno de los dominios válidos
        if not any(re.search(pattern, email) for pattern in valid_domains):
            raise ValidationError("Por favor, introduce un correo electrónico con un dominio válido, como @gmail.com, @hotmail.com o un dominio propio.")
        
        return email    