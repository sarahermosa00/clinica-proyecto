from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Sum, Q
from django.db import transaction
from django.http import JsonResponse
from decimal import Decimal
from factura.models.modelo_factura import Factura, DetalleFactura

from ..forms import FormularioFactura, DetalleFactura, DetalleFacturaFormSet, FormularioDetalleFactura






# ------vista de factura--------
# para crear una nueva pantalla con los datos del modelo de factura

class PantallaFactura(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clinica/factura/pantalla_factura.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')
        facturas = Factura.objects.all()
        # para el filtro aca debo añadir cliente proveedor y la razon social porque estos campos son foraneos
        contexto['facturas'] = facturas.order_by('cliente_proveedor__razon_social')
        # el filtro para la busqueda
        if query:
            facturas = facturas.filter(
                Q(cliente_proveedor__razon_social__icontains=query) 
               
            )
        contexto['facturas'] =  facturas.order_by('cliente_proveedor__razon_social')
        contexto['query'] = query
        return contexto
    




# ------------------Agregar-------------------  
# lo que se va agregar es una nueva factura entera, lo del detall no se como va ir


class AgregarFactura(LoginRequiredMixin, generic.CreateView):
    """Añade una nueva factura"""
    model = Factura
    form_class = FormularioFactura
    template_name = 'clinica/factura/form_create_factura.html'  


    def get_success_url(self):
        messages.success(self.request, "Factura creada con éxito")
        return reverse_lazy('factura:pantalla_factura')  


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Agregar Producto'
        contexto['encabezado'] = 'Agregar nuevo producto'
        try:
            
            if self.request.POST:
                contexto['detalle_factura_formset'] = DetalleFacturaFormSet(self.request.POST)
            else:
                contexto['detalle_factura_formset'] = DetalleFacturaFormSet()   
            return contexto
        

        except Exception as e:
            print(f"Error en agregar factura en la vista. Error al cargar el formulario: {str(e)}")   
            return JsonResponse({'error': str(e)}, status=500)




    def form_valid(self, form):




        contexto =  self.get_context_data()
        detalle_factura_formset = contexto['detalle_factura_formset']
        with transaction.atomic():
            try:
                self.object = form.save()
                if detalle_factura_formset.is_valid():
                    detalle_factura_formset.instance = self.object
                    detalle_factura_formset.save()
                else:
                    print(detalle_factura_formset.errors)   
                    # raise Exception("No se pudo insertar el detalle")   
                    return self.form_invalid(form)
                # no me esta mostrando correctamente el error 
            except Exception as e:
           
                print(f"Error capturado en la validaciòn del form de la vista. Error al guardar la factura : {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)


        return super().form_valid(form)




# -----------------DetalleFactura------------------




# -------------mirar detalles---------------
class DetallaFactura(LoginRequiredMixin, generic.DetailView):
    model = Factura
    template_name = "clinica/factura/detalle_factura.html"
    context_object_name = "factura"


    def dispatch(self, request, *args, **kwargs):
        print(self.request.POST)
        return super().dispatch(request, *args, **kwargs)
    


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        factura = kwargs['object']
        print("Imprimiendo la factura")
        print(factura)
        detalle_factura = factura.detallefactura_set.all()
        detalle_factura = DetalleFactura.objects.filter(factura=self.object)  
        subtotal = sum(detalle_factura.precio * detalle_factura.cantidad for detalle_factura in detalle_factura.all())

        iva = subtotal * Decimal(0.10)  
        total_con_iva = subtotal + iva
        contexto["subtotal"] = subtotal
        contexto["iva"] = iva
        contexto["total_con_iva"] = total_con_iva
        contexto['detalle_factura'] = detalle_factura
        
       
        
        return contexto
