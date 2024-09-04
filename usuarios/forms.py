# Django
from django.contrib.auth.forms import UserCreationForm

# Modelos
from .models import Usuario

class FormularioUsuario(UserCreationForm):

    class Meta:
        model = Usuario
        fields = (
            'username', 'password1', 'password2', 'rol', 'nombre', 'apellido', 'imagen', 'email', 'documento'
            )
    #para filtrar en el form de crear usuario solo los roles creados hasta el release 1    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones del campo 'rol' para mostrar solo 'Medico' y 'Secretaria'
        self.fields['rol'].queryset = Usuario._meta.get_field('rol').choices  # Filtra solo las opciones predefinidas
        self.fields['rol'].choices = [choice for choice in Usuario._meta.get_field('rol').choices if choice[0] in ['S', 'M']]