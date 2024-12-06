from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Sum, Q
from django.core.paginator import Paginator


from factura.models.modelo_proveedor import Proveedor
from usuarios.models import registrarActividad

from ..forms import FormularioProveedor

# ---------panalla principal de proveedores------------
class PantallaProveedor(LoginRequiredMixin, generic.TemplateView):
    # no funciona la paginacion porque el generic template view no lo gestiona
    template_name = 'clinica/factura/pantalla_proveedor.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        # para buscar hay que colocar obtener el query y de donde, en este caso la url, que como esta vacioo es ahi mismo donde buscamos
        query = self.request.GET.get('query', '') 
        proveedores = Proveedor.objects.all()
        if query:  
            proveedores = proveedores.filter(
                Q(razon_social__icontains=query) |  
                Q(ruc__icontains=query)            
            ).order_by('razon_social')  

        paginator = Paginator(proveedores,self.paginate_by)
        numero_pagina =  self.request.GET.get('page')
        objeto_pagina = paginator.get_page(numero_pagina)       

        contexto['buscar'] = 'Buscar clientes por RUC o razón social'
        contexto['proveedores'] = objeto_pagina
        contexto['query'] = query  

        return contexto


# -------------------pantalla a la cual va cuando le doy a detalles--------------------

class DetallaProveedor(LoginRequiredMixin, generic.DetailView):
    # aca hereda de LoginRequiredMixin y generic.DeleteView
    # sobreescribe los metodos para decirle aca quiero que uses este modelo y no el generico, los metodos siguientes tambien se sobre escriben para especificidad y no usar los por defecto
    model = Proveedor 
    template_name = 'clinica/factura/detalle_proveedores.html'
    context_object_name = 'proveedor'  
    # context_object_name es el nombre que se usa en el html 
    paginate_by = 5   
    # para que muestre 5 resultados por pagina



    def get_context_data(self, **kwargs):

        contexto =super().get_context_data(**kwargs)
        contexto['razon_social'] = self.object.razon_social
        contexto['ruc'] = self.object.ruc
        contexto['telefono'] = self.object.telefono
        contexto['direccion'] = self.object.direccion
        contexto['tipo'] = self.object.tipo
        contexto['estado'] = self.object.estado
      


        return contexto





# ------------------Agregar-------------------



class Agregar(LoginRequiredMixin, generic.CreateView):
    """Añadir un nuevo proveedor"""
    model = Proveedor
    form_class = FormularioProveedor
    template_name = 'clinica/factura/form_create.html'
    paginate_by = 5

    def get_success_url(self):
        return reverse_lazy('factura:pantalla_proveedor')

    def form_valid(self, form):
        proveedor = form.save()  
        print(proveedor)
        messages.success(self.request, 'Preveedor generado con exito.')
        return super().form_valid(form)
    

# --------------editar------------------------------------

class Editar(LoginRequiredMixin, generic.UpdateView):
    model = Proveedor
    form_class = FormularioProveedor
    template_name = 'clinica/factura/form_create.html'
    paginate_by = 5


    # def get_success_url(self):
    #     return reverse_lazy('factura:pantalla_proveedor')

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Modificó un proveedor'
        )
        messages.success(
            self.request,
            'Proveedor modificado!'
        )
    

        ruta = self.request.META['HTTP_REFERER']
        proveedor_uuid = ruta.split('/').pop()
        return reverse_lazy('factura:detalle_proveedores', kwargs={'pk': proveedor_uuid})
        # tiene que volver a una pantalla que tenga un id

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Editar a {self.object.razon_social}'
        contexto['editar'] = True
        return contexto



# ---------------------------Eliminar----------------------------------

class Eliminar(LoginRequiredMixin, generic.DeleteView):
    model = Proveedor
    template_name = 'componentes/delete.html'
    paginate_by = 5

    # esta funcion retorna el template donde vos queres que se vaya si la eliminacion se hizo correctamente, en este caso en la pantalla de proveedores donde se muestra la lista de los proveedores que quedan
    
    def get_success_url(self):
        return reverse_lazy('factura:pantalla_proveedor')
    

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó un proveedor'
        )
        messages.success(
            self.request,
            'Proveedor eliminado!'
        )
        return reverse_lazy('factura:pantalla_proveedor')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar {self.object.razon_social}'
        contexto['url_volver'] = reverse_lazy('factura:pantalla_proveedor')
        return contexto
