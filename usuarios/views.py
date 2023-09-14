# Django
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.timezone import localtime, now
from django.contrib.auth.views import LoginView, LogoutView

# Modelos
from .models import Usuario, ROL_OPCIONES, Actividad
from django.contrib.auth.models import Group

# Formularios
from .forms import FormularioUsuario

class IniciarSesion(LoginView):
    template_name = 'clinica/usuarios/inicio_de_sesion.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('compartido:inicio')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        usuario = self.request.user.username
        ultima_vez = localtime(self.request.user.last_login).date()
        fecha_registro = localtime(self.request.user.date_joined).date()
        if fecha_registro == ultima_vez:
            messages.success(
                self.request,
                f'Hola {usuario}! que tengas un productivo primer dia en el sistema! 🥳'
            )
        else:
            messages.success(
                self.request,
                f'Hola {usuario}! entraste por ultima vez el {ultima_vez}'
            )
        if self.request.user.groups.exists():
            grupo = self.request.user.groups.get()
            if grupo.name == ROL_OPCIONES[0][1]:
                # Medico
                return reverse_lazy('pacientes:lista')
            elif grupo.name == ROL_OPCIONES[1][1]:  
                # SECRETARIA
                return reverse_lazy('pacientes:lista_turnos')
            elif grupo.name == ROL_OPCIONES[2][1]:  
                # Gerencia
                return reverse_lazy('productos:lista')
            elif grupo.name == ROL_OPCIONES[3][1]:  
                # Venta
                return reverse_lazy('productos:lista_pedidos')
            elif grupo.name == ROL_OPCIONES[4][1]:  
                # Taller
                return reverse_lazy('productos:lista_pedidos')
        return reverse_lazy('productos:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Iniciar Sesión'
        return ctx


class CrearUsuario(generic.CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'clinica/usuarios/form_usuario.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('compartido:inicio')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_staff = True
        form.instance.is_active = True
        return super().form_valid(form)
    
    def get_success_url(self):
        nombre_usuario = self.request.POST.get('username')
        usuario = Usuario.objects.get(username=nombre_usuario)
        grupo = Group.objects.get(name=usuario.get_rol_display())
        usuario.groups.add(grupo.id)
        messages.success(
            self.request,
            f'Usuario {nombre_usuario} registrado!'
        )
        return reverse_lazy('usuarios:entrar')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Crear usuario'
        return ctx


class ListaActividades(generic.ListView):
    queryset = Actividad.objects.order_by('-id')
    template_name = 'clinica/usuarios/actividades.html'
    context_object_name = 'Actividades'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Registro de actividades'
        ctx['buscar'] = 'Nombre de usuario o actividad'
        return ctx


class ListaUsuarios(generic.ListView):
    queryset = Usuario.objects.order_by('-date_joined')
    template_name = 'clinica/usuarios/lista_usuarios.html'
    context_object_name = 'Usuarios'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Lista de usuarios'
        ctx['buscar'] = 'Nombre de usuario o sector'
        return ctx