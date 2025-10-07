from django import forms
from .models import ConversionDivisa

class ConversionDivisaForm(forms.ModelForm):
    class Meta:
        model = ConversionDivisa
        fields = ['tipo_operacion', 'monto_origen', 'monto_destino', 'tasa_usd', 'descripcion']
        widgets = {
            'fecha_conversion': forms.DateInput(attrs={'type': 'date'}),
        }