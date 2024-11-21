# Django
from django.urls import path


# Vistas 
# el nombre del archivo de la vista es el que se importa
from .views import proveedores, objetos, factura


app_name = 'factura'


URLS_PROVEEDORES = [
    path('factura/', proveedores.PantallaProveedor.as_view(), name='pantalla_proveedor'),
    path('detalle/<int:pk>', proveedores.DetallaProveedor.as_view(), name='detalle_proveedores'),
    path('editar/<int:pk>', proveedores.Editar.as_view(), name='editar_proveedor'),
    path('eliminar/<int:pk>', proveedores.Eliminar.as_view(), name='eliminar_proveedor'),
    # path('', proveedores.Listar.as_view(), name='lista'),
    path('agregar/', proveedores.Agregar.as_view(), name='agregar_proveedor'),
    
    
]

URLS_OBJETOS = [

    # la url aca debe ser diferente, el nombre que se le pone puede ser cualquiera
    path('objetofactura/', objetos.PantallaObjetos.as_view(), name='pantalla_objetos'),
    path('detalleobjeto/<uuid:pk>', objetos.DetalleObjeto.as_view(), name='detalle_objetos'),
    path('agregarobjeto/', objetos.AgregarObjeto.as_view(), name='agregar_objeto'),
    path('editar_objeto/<uuid:pk>', objetos.EditarObjeto.as_view(), name='editar_objeto'),
    
]

URLS_FACTURAS = [
    path('pantallafactura/', factura.PantallaFactura.as_view(), name='pantalla_factura'),
    path('facturagregar/', factura.AgregarFactura.as_view(), name='agregar_factura'),
    path('detalle_factura/<uuid:pk>', factura.DetallaFactura.as_view(), name='detalle_factura'),

]

urlpatterns = URLS_PROVEEDORES + URLS_OBJETOS + URLS_FACTURAS
