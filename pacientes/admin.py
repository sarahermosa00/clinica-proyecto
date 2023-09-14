# Django
from django.contrib import admin

# Modelos
from .models import *

@admin.register(Paciente, Observacion, Turno)
class AplicacionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')