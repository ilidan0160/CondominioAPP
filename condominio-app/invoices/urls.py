from django.urls import path
from . import views

urlpatterns = [
    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('generar/', views.generar_factura, name='generar_factura'),
    path('generar-alicuotas/', views.generar_facturas_alicuotas, name='generar_facturas_alicuotas'),
    path('crear/', views.crear_factura, name='crear_factura'),
]