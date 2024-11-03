from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Sum, Q
from usuarios.models import registrarActividad
from factura.models.modelo_objeto import ObjetoFactura
from ..forms import FormularioObjeto





# -----------Vista principal-------------

class PantallaObjetos(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clinica/factura/pantalla_objetos.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        objetos = ObjetoFactura.objects.all()


        contexto['objetos'] = objetos.order_by('-codigo_objeto')

        return contexto
    

# -----------------vista de detalle de objetos--------------


class DetalleObjeto(LoginRequiredMixin, generic.DetailView):
    model = ObjetoFactura
    template_name = 'clinica/factura/detalle_objetos.html'
    context_object_name = 'objeto'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nombre_objeto'] = self.object.nombre_objeto
        contexto['codigo_objeto'] = self.object.codigo_objeto
        contexto['precio_objeto'] = self.object.precio_objeto
        

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
