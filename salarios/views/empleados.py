# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, Q
from django.views import generic

# Modelos
from ..models import Empleado, Categoria
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioEmpleado


class Listar(LoginRequiredMixin, generic.ListView):
    """
    Lista todos los productos cargados en el sistema. 
    """
    model = Empleado
    template_name = 'clinica/salarios/lista_empleados.html'
    context_object_name = 'Empleados'
    paginate_by = 5
    # page_kwarg

    def get_queryset(self):
        q_busqueda = self.request.GET.get('query')
        q_categoria_nombre = self.request.GET.get('categoria')
        if q_busqueda:
            return Empleado.objects.filter(
                Q(nombre__in=q_busqueda.split()) | Q(nombre__icontains=q_busqueda.split()[0])
            )
        if q_categoria_nombre:
            q_categoria = Categoria.objects.get(nombre=q_categoria_nombre)
            return Empleado.objects.filter(categoria=q_categoria.id)    
        return Empleado.objects.all()

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Lista de empleados'
        contexto['buscar'] = 'Ingresa el nombre de alǵun empleado'
        contexto['categorias'] = Categoria.objects.all()
        return contexto


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega un nuevo empleado y retorna a la lista de empleados.
    """
    model = Empleado
    form_class = FormularioEmpleado
    template_name = 'clinica/salarios/form_empleado.html'
    success_url = reverse_lazy('salarios:lista')

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Cargó un empleado'
        )
        messages.success(
            self.request,
            'Empleado cargado!'
        )
        path_previo = self.request.GET.get('prev')
        # Si accedemos desde detalle empleado, volverá al detalle
        if path_previo:
            empleado_id = path_previo.split('/').pop()
            return reverse_lazy('salarios:detalle_empleado', kwargs={'pk':empleado_id})
        else:
            # Si no, vuelve a lista de empleados
            return reverse_lazy('salarios:lista')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Agregar empleados'
        return contexto



class Detalle(LoginRequiredMixin, generic.DetailView):
    """ 
    Muestra toda la información de un determinado empleado.
    """
    model = Empleado
    template_name = 'clinica/salarios/detalle_empleado.html'
    context_object_name = 'Empleado'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = self.object
        contexto['cantidad'] = Empleado.objects.count()
        return contexto


class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de un determinado empleado.
    """
    model = Empleado
    form_class = FormularioEmpleado
    template_name = 'clinica/salarios/form_empleado.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Modificó un empleado'
        )
        messages.success(
            self.request,
            'Empleado modificado!'
        )
        ruta = self.request.META['HTTP_REFERER']
        empleado_uuid = ruta.split('/').pop()
        return reverse_lazy('salarios:detalle_empleado', kwargs={'pk': empleado_uuid})

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Editar a {self.object}'
        contexto['editar'] = True
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """ 
    Elimina un empleado del sistema.
    """
    model = Empleado
    template_name = 'componentes/delete.html'
    
    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó un empleado'
        )
        messages.success(
            self.request,
            'Empleado eliminado!'
        )
        return reverse_lazy('salarios:lista')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'eliminar a {self.object.nombre.upper()}'
        contexto['url_volver'] = reverse_lazy('salarios:lista')
        return contexto