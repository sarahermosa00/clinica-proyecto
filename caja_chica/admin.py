# Django
from django.contrib import admin

# Modelos
from .models import *

@admin.register(MovimientoCajaChica)
class AplicacionAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha', 'creado_en')

admin.site.register(SaldoDiarioCajaChica)