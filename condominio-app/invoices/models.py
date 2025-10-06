from django.db import models
from core.models import Unidad, ConfiguracionGeneral

class Factura(models.Model):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    monto_total_usd = models.FloatField()
    monto_total_bs_fecha_emision = models.FloatField()
    tasa_usd_fecha_emision = models.FloatField()
    fecha_emision = models.DateField() 
    pagada = models.BooleanField(default=False)

    def saldo_pendiente_bs(self):
        pagos = Pago.objects.filter(unidad=self.unidad, fecha_pago__gte=self.fecha_emision)
        total_pagado_bs = sum(p.monto_pagado_bs for p in pagos)
        return self.monto_total_bs_fecha_emision - total_pagado_bs

    def saldo_pendiente_usd(self):
        tasa_actual = ConfiguracionGeneral.objects.last().tasa_cambio_actual
        saldo_bs = self.saldo_pendiente_bs()
        return saldo_bs / tasa_actual

    def __str__(self):
        return f"Factura {self.unidad.nombre} - {self.fecha_emision}"