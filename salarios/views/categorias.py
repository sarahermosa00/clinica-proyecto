# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic

# Modelos
from ..models import Categoria, Empleado
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioCategoria


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega una nueva categoria.
    """
    model = Categoria
    form_class = FormularioCategoria
    template_name = 'clinica/salarios/categorias.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Cargó una categoria'
        )
        messages.success(
            self.request,
            'Categoria cargada!'
        )
        return reverse_lazy('salarios:categorias')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Categorias'
        contexto['categorias'] = Categoria.objects.all()
        return contexto



class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de una determinada categoria.
    """
    model = Categoria
    form_class = FormularioCategoria
    template_name = 'clinica/salarios/categorias.html'       

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Modificó una categoria'
        )
        messages.success(
            self.request,
            'Categoria modificada!'
        )
        return reverse_lazy('salarios:categorias') 

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Categorias'
        contexto['editar'] = True
        contexto['empleados'] = Empleado.objects.filter(categoria=self.kwargs['pk'])
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """ 
    Elimina una categoria del sistema.
    """
    model = Categoria
    template_name = 'componentes/delete.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó una categoria'
        )
        messages.success(
            self.request,
            'Categoria eliminada!'
        )
        return reverse_lazy('salarios:categorias')


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar {self.object}'
        contexto['url_volver'] = reverse_lazy('salarios:categorias')
        return contexto