from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ConversionDivisa

@login_required
def lista_conversiones(request):
    conversiones = ConversionDivisa.objects.all()
    context = {
        'conversiones': conversiones
    }
    return render(request, 'accounts/lista_conversiones.html', context)