from django import forms
from .models import Gasto, CategoriaGasto, Pago, CuotaEspecial
from core.models import Unidad

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['descripcion', 'categoria', 'monto_usd', 'monto_bs', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['unidad', 'monto_pagado_bs', 'monto_pagado_usd', 'tasa_usd_fecha_pago', 'fecha_pago', 'metodo_pago', 'estado']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }

class CuotaEspecialForm(forms.ModelForm):
    class Meta:
        model = CuotaEspecial
        fields = ['descripcion', 'monto_usd', 'monto_bs', 'fecha', 'unidades', 'aplicar_a_todas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }