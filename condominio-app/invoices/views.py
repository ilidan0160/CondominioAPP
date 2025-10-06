from django.contrib.auth.decorators import login_required
from .models import Factura
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Unidad, Gasto, ConfiguracionGeneral
from .forms import FacturaForm

@login_required
def lista_facturas(request):
    facturas = Factura.objects.all()
    context = {
        'facturas': facturas
    }
    return render(request, 'invoices/lista_facturas.html', context)

@login_required
def generar_factura(request):
    if request.method == 'POST':
        unidad_id = request.POST.get('unidad')
        monto_usd = request.POST.get('monto_usd')

        try:
            unidad = Unidad.objects.get(id=unidad_id)
            monto_usd = float(monto_usd)

            # Obtener la tasa actual
            config = ConfiguracionGeneral.objects.last()
            tasa = config.tasa_cambio_actual if config else 1

            # Calcular monto en Bs
            monto_bs = monto_usd * tasa

            # Crear la factura
            Factura.objects.create(
                unidad=unidad,
                monto_total_usd=monto_usd,
                monto_total_bs_fecha_emision=monto_bs,
                tasa_usd_fecha_emision=tasa
            )

            messages.success(request, f'Factura generada para {unidad.nombre}.')
            return redirect('generar_factura')
        except Unidad.DoesNotExist:
            messages.error(request, 'Unidad no válida.')
        except ValueError:
            messages.error(request, 'Monto no válido.')
    else:
        unidades = Unidad.objects.all()

    return render(request, 'invoices/generar_factura.html', {'unidades': unidades})

@login_required
def generar_facturas_alicuotas(request):
    if request.method == 'POST':
        # Obtener gastos del mes actual
        from datetime import date
        gastos = Gasto.objects.filter(fecha__month=date.today().month)

        # Calcular total de gastos comunes
        total_gastos = sum(g.monto_usd for g in gastos)

        # Obtener todas las unidades
        unidades = Unidad.objects.all()

        # Obtener tasa actual
        config = ConfiguracionGeneral.objects.last()
        tasa = config.tasa_cambio_actual if config else 1

        # Recorrer cada unidad y generar factura
        for unidad in unidades:
            monto_usd = (unidad.alicuota / 100) * total_gastos
            monto_bs = monto_usd * tasa

            Factura.objects.create(
                unidad=unidad,
                monto_total_usd=monto_usd,
                monto_total_bs_fecha_emision=monto_bs,
                tasa_usd_fecha_emision=tasa
            )

        messages.success(request, f'Se generaron {len(unidades)} facturas.')
        return redirect('generar_facturas_alicuotas')

    return render(request, 'invoices/generar_facturas_alicuotas.html')

@login_required
def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save()
            messages.success(request, f'Factura para "{factura.unidad.nombre}" creada exitosamente.')
            return redirect('crear_factura')
    else:
        form = FacturaForm()

    return render(request, 'invoices/crear_factura.html', {'form': form})