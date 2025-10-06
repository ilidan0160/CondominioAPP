from django import forms
from .models import Factura
from core.models import Unidad, ConfiguracionGeneral

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['unidad', 'monto_total_usd', 'monto_total_bs_fecha_emision', 'tasa_usd_fecha_emision', 'fecha_emision']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener la tasa actual para usarla como valor por defecto
        config = ConfiguracionGeneral.objects.last()
        if config:
            self.fields['tasa_usd_fecha_emision'].initial = config.tasa_cambio_actual

