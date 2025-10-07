from django.urls import path
from . import views

urlpatterns = [
    path('conversiones/', views.lista_conversiones, name='lista_conversiones'),
    path('conversiones/crear/', views.crear_conversion_divisa, name='crear_conversion_divisa'),  # ← Agrega esta línea
]