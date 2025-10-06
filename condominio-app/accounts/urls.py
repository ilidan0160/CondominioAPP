from django.urls import path
from . import views

urlpatterns = [
    path('conversiones/', views.lista_conversiones, name='lista_conversiones'),
]