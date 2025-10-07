from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ConversionDivisa
from .forms import ConversionDivisaForm
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def lista_conversiones(request):
    conversiones = ConversionDivisa.objects.all().order_by('-fecha_conversion')
    context = {
        'conversiones': conversiones
    }
    return render(request, 'accounts/lista_conversiones.html', context)

@login_required
def crear_conversion_divisa(request):
    if request.method == 'POST':
        form = ConversionDivisaForm(request.POST)
        if form.is_valid():
            conversion = form.save()
            messages.success(request, f'Conversión registrada: {conversion}.')
            return redirect('crear_conversion_divisa')
    else:
        form = ConversionDivisaForm()

    return render(request, 'accounts/crear_conversion_divisa.html', {'form': form})