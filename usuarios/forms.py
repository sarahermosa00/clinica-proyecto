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