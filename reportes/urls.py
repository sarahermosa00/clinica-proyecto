# Django
from django.urls import path

# Vistas
from .views import ListaPacientes, ListaVentasPorMes, ListaPagosPorMes, ListaMovimientosCajaPorMes, descargarPDF

app_name = 'reportes'

urlpatterns = [
    path('pacientes/',ListaPacientes.as_view(), name='pacientes'),
    path('ventas/', ListaVentasPorMes.as_view(), name='ventas'),
    path('salarios/', ListaPagosPorMes.as_view(), name='salarios'),
    path('caja/', ListaMovimientosCajaPorMes.as_view(), name='caja'),
    path('descargar/', descargarPDF, name='descargar')
]