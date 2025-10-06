from django.contrib import admin
from .models import Factura

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['unidad', 'monto_total_usd', 'fecha_emision', 'pagada']