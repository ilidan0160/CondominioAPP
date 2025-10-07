from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('mis-facturas/', views.mis_facturas, name='mis_facturas'),
    path('mis-pagos/', views.ver_pagos_propietario, name='ver_pagos_propietario'),
    path('saldos-pendientes/', views.ver_saldos_pendientes, name='ver_saldos_pendientes'), 
    path('gastos/', views.lista_gastos, name='lista_gastos'),
    path('gastos/crear/', views.crear_gasto, name='crear_gasto'),
    path('gastos/editar/<int:id>/', views.editar_gasto, name='editar_gasto'),
    path('pagos/crear/', views.crear_pago, name='crear_pago'),
    path('cuotas-especiales/', views.lista_cuotas_especiales, name='lista_cuotas_especiales'),
    path('cuotas-especiales/crear/', views.crear_cuota_especial, name='crear_cuota_especial'),
    path('actualizar-tasa/', views.actualizar_tasa_api, name='actualizar_tasa_api'),
    path('actualizar-tasa-manual/', views.actualizar_tasa_manual, name='actualizar_tasa_manual'),
     path('enviar-estado-cuenta/', views.enviar_estado_cuenta, name='enviar_estado_cuenta'), 
     path('enviar-estado-cuenta-telegram/', views.enviar_estado_cuenta_telegram, name='enviar_estado_cuenta_telegram'),
     path('factura-pdf/<int:id>/', views.generar_factura_pdf, name='generar_factura_pdf'),
]