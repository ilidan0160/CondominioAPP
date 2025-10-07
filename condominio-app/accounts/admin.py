from django.contrib import admin
from .models import ConversionDivisa

@admin.register(ConversionDivisa)
class ConversionDivisaAdmin(admin.ModelAdmin):
    list_display = ['fecha_conversion', 'monto_origen', 'monto_destino', 'tasa_usd', 'descripcion']