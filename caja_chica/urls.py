# Django
from django.urls import path

# Vistas
from .views import caja

app_name = 'caja_chica'

URLS_CAJA_CHICA = [
    path('', caja.ListaMovimientosCajaChica.as_view(), name='lista_movimientos'),
    path('crear-saldo/', caja.CrearSaldoDiario.as_view(), name='crear_saldo'),
    path('exportar_pdf/', caja.exportar_pdf, name='exportar_pdf'),
    path('cerrar_caja/', caja.CerrarCaja.as_view(), name='cerrar_caja'),
    path('gestionar_caja/', caja.gestionar_caja, name='gestionar_caja'),

]



urlpatterns = URLS_CAJA_CHICA