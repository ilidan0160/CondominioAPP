from django.db import models

class ConversionDivisa(models.Model):
    fecha_conversion = models.DateField(auto_now_add=True)
    tipo_operacion = models.CharField(max_length=10, choices=[
        ('compra', 'Compra de USD (Bs → USD)'),
        ('venta', 'Venta de USD (USD → Bs)'),
    ], default='compra')  # ← Agregamos un valor por defecto
    monto_origen = models.FloatField()  # Bs si compra, USD si vende
    monto_destino = models.FloatField() # USD si compra, Bs si vende
    tasa_usd = models.FloatField()
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        if self.tipo_operacion == 'compra':
            return f"Compra: {self.monto_origen} Bs → {self.monto_destino} USD (Tasa: {self.tasa_usd})"
        else:
            return f"Venta: {self.monto_origen} USD → {self.monto_destino} Bs (Tasa: {self.tasa_usd})"