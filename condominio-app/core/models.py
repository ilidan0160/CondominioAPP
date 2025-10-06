from django.db import models
from django.contrib.auth.models import User

class ConfiguracionGeneral(models.Model):
    tasa_cambio_actual = models.FloatField()
    fecha_actualizacion_tasa = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Tasa: {self.tasa_cambio_actual}"

class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    nombre = models.CharField(max_length=50)
    alicuota = models.FloatField()
    propietario = models.CharField(max_length=100)
    inquilino = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Pago(models.Model):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    monto_pagado_bs = models.FloatField()
    monto_pagado_usd = models.FloatField()
    tasa_usd_fecha_pago = models.FloatField()
    fecha_pago = models.DateField() 
    metodo_pago = models.CharField(max_length=20, choices=[
        ('bs', 'Bs.F'),
        ('usd', 'USD'),
    ])
    estado = models.CharField(max_length=20, default='pagado')

    def __str__(self):
        return f"Pago de {self.unidad.nombre} - {self.monto_pagado_bs} Bs"

class Gasto(models.Model):
    descripcion = models.CharField(max_length=200)
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE)
    monto_usd = models.FloatField()
    monto_bs = models.FloatField()  # Calculado con tasa del día
    fecha = models.DateField()  # ← Cambia esta línea

    def __str__(self):
        return f"{self.descripcion} - {self.monto_usd} USD"

class CuotaEspecial(models.Model):
    descripcion = models.CharField(max_length=200)
    monto_usd = models.FloatField()
    monto_bs = models.FloatField()  # Calculado con tasa del día
    fecha = models.DateField()  # ← Cambia esta línea
    unidades = models.ManyToManyField(Unidad, blank=True)  # Puede aplicar a varias unidades
    aplicar_a_todas = models.BooleanField(default=False)  # Si es True, aplica a todas las unidades

    def __str__(self):
        return f"{self.descripcion} - {self.monto_usd} USD"