# Django
from django.urls import path

# Vistas
from .views import caja

app_name = 'caja_chica'

URLS_CAJA_CHICA = [
    path('', caja.ListaMovimientosCajaChica.as_view(), name='lista_movimientos'),
    path('crear-saldo/', caja.CrearSaldoDiario.as_view(), name='crear_saldo'),
    path('exportar_pdf/', caja.exportar_pdf, name='exportar_pdf'),

    # path('detalle/<uuid:pk>', empleados.Detalle.as_view(), name='detalle_empleado'),
    # path('editar/<uuid:pk>', empleados.Editar.as_view(), name='editar_empleado'),
    # path('eliminar/<uuid:pk>', empleados.Eliminar.as_view(), name='eliminar_empleado'),
]



urlpatterns = URLS_CAJA_CHICA