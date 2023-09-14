# Django
from django.urls import path

# Vistas
from .views import *

app_name = 'usuarios'

urlpatterns = [
    path('', IniciarSesion.as_view(), name='entrar'),
    path('salir/', LogoutView.as_view(), name='salir'),
    path('crear/', CrearUsuario.as_view(), name='crear'),
    path('lista/', ListaUsuarios.as_view(), name='lista'),
    path('actividades/', ListaActividades.as_view(), name='actividades')
]