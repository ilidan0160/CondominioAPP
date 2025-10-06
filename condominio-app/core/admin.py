from django.contrib import admin
from .models import ConfiguracionGeneral, Unidad, Pago, CategoriaGasto, Gasto, CuotaEspecial 

@admin.register(ConfiguracionGeneral)
class ConfiguracionGeneralAdmin(admin.ModelAdmin):
    list_display = ['tasa_cambio_actual', 'fecha_actualizacion_tasa']

@admin.register(CategoriaGasto)
class CategoriaGastoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'propietario', 'inquilino', 'usuario']

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['unidad', 'monto_pagado_bs', 'fecha_pago', 'metodo_pago']

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'categoria', 'monto_usd', 'monto_bs', 'fecha']

@admin.register(CuotaEspecial)
class CuotaEspecialAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'monto_usd', 'monto_bs', 'fecha', 'aplicar_a_todas']
    filter_horizontal = ['unidades']  # Permite seleccionar varias unidades