from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Sum, Q
from usuarios.models import registrarActividad
from factura.models.modelo_objeto import ObjetoFactura
from ..forms import FormularioObjeto
from django.core.paginator import Paginator





# -----------Vista principal-------------

class PantallaObjetos(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clinica/factura/pantalla_objetos.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        objetos = ObjetoFactura.objects.all()
        paginator = Paginator(objetos,self.paginate_by)
        numero_pagina =  self.request.GET.get('page')
        objeto_pagina = paginator.get_page(numero_pagina)   
        contexto['buscar'] = 'Buscar productos por nombre'
        contexto['objetos'] = objeto_pagina


        return contexto
    

# -----------------vista de detalle de objetos--------------


class DetalleObjeto(LoginRequiredMixin, generic.DetailView):
    model = ObjetoFactura
    template_name = 'clinica/factura/detalle_objetos.html'
    context_object_name = 'objeto'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nombre_objeto'] = self.object.nombre_objeto
        contexto['codigo_objeto'] = self.object.codigo_objeto
        contexto['precio_objeto'] = self.object.precio_objeto
        contexto['estado_objeto'] = self.object.estado_objeto
        
        

        return contexto
    


# ------------------agregar------------------------

class AgregarObjeto(LoginRequiredMixin, generic.CreateView):
    model = ObjetoFactura
    form_class = FormularioObjeto
    template_name = 'clinica/factura/form_create_objeto.html'


    def get_success_url(self):
        return reverse_lazy('factura:pantalla_objetos')
    

    def form_valid(self, form):
        objeto = form.save()
        messages.success(self.request, 'Objeto generado con exito')
        return super().form_valid(form)
    


# --------------editar------------------------------------
class EditarObjeto(LoginRequiredMixin, generic.UpdateView):
    model = ObjetoFactura
    form_class = FormularioObjeto
    # el editar debe estar en el mismo donde se hace el create
    template_name = 'clinica/factura/form_create_objeto.html'



    def get_success_url(self):
        registrarActividad(
            self.request,
            'Se modifico un objeto'
        )
        messages.success(
            self.request,
            'Objeto modificado'
        )


        ruta = self.request.META['HTTP_REFERER']
        objeto_uuid = ruta.split('/').pop()
        return reverse_lazy('factura:detalle_objetos', kwargs={'pk':objeto_uuid})



    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        #aca si solo se le pone editar al self.object trae toda la representacion del objeto, por eso le especifico un atributo que en este caso es su nombre para que sea el que se muestre
        contexto['titulo'] = f'Editar a {self.object.nombre_objeto}'
        contexto['editar'] = True
        return contexto
    

#-----------------------Eliminar-------------------------


class EliminarObjeto(LoginRequiredMixin, generic.DeleteView):
    model = ObjetoFactura
    template_name = 'componentes/delete.html'
    paginate_by = 5


    def get_success_url(self):
        return reverse_lazy('factura:pantalla_objetos')
    
    def get_context_data(self):
        registrarActividad(
            self.request,
            'Se elimino un producto'
        )   
        messages.success(
            self.request,
            'Producto eliminado'
        )
        return reverse_lazy('factura:pantalla_objetos')
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar {self.object.nombre_objeto}'
        contexto['url_volver'] = reverse_lazy('factura:pantalla_objetos')
        return contexto
    


