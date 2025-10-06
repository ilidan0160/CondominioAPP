from django.db import models

class ConversionDivisa(models.Model):
    fecha_conversion = models.DateField(auto_now_add=True)
    monto_bs = models.FloatField()
    monto_usd = models.FloatField()
    tasa_usd = models.FloatField()
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.fecha_conversion} - {self.monto_bs} Bs → {self.monto_usd} USD"