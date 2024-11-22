# Django
from django.urls import path

# Vistas
from .views import empleados, categorias, salarios

app_name = 'salarios'

URLS_EMPLEADOS = [
    path('', empleados.Listar.as_view(), name='lista'),
    path('agregar/', empleados.Agregar.as_view(), name='agregar_empleado'),
    path('detalle/<uuid:pk>', empleados.Detalle.as_view(), name='detalle_empleado'),
    path('editar/<uuid:pk>', empleados.Editar.as_view(), name='editar_empleado'),
    path('eliminar/<uuid:pk>', empleados.Eliminar.as_view(), name='eliminar_empleado'),
]

URLS_CATEGORIAS = [
    path('categorias/', categorias.Agregar.as_view(), name='categorias'),
    path('categorias/editar/<int:pk>', categorias.Editar.as_view(), name='editar_categoria'),
    path('categorias/eliminar/<int:pk>', categorias.Eliminar.as_view(), name='eliminar_categoria')
]
# URLs para salarios
URLS_SALARIOS = [
    path('salarios/', salarios.PantallaSalarios.as_view(), name='pantalla_salarios'),
    path('salarios/generar/', salarios.GenerarPagoSalario.as_view(), name='generar_pago'),
    path('salarios/listar/', salarios.ListarPagosSalarios.as_view(), name='listar_pagos'),
    path('salarios/detalle/<uuid:pk>/', salarios.DetallePagoSalario.as_view(), name='detalle_pago_salario'),
    path('salarios/exportar/<uuid:pk>/', salarios.exportar_pago_xlsx, name='exportar_xlsx'),
    path('salarios/exportarpdf/<uuid:pk>/', salarios.exportar_pago_pdf, name='exportar_pdf'),

]

urlpatterns = URLS_EMPLEADOS + URLS_CATEGORIAS + URLS_SALARIOS