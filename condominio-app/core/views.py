from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ConfiguracionGeneral, Unidad, Pago, CategoriaGasto, Gasto, CuotaEspecial
from invoices.models import Factura
from .forms import GastoForm, PagoForm, CuotaEspecialForm
import requests
from django.core.mail import send_mail
from django.conf import settings
import telegram
from reportlab.pdfgen import canvas
from django.http import HttpResponse

@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, 'core/admin_dashboard.html')
        else:
            return render(request, 'core/user_dashboard.html')
    else:
        return render(request, 'dashboard.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')  # Redirigir si ya está logueado
        return super().dispatch(request, *args, **kwargs)

@login_required
def mi_cuenta(request):
    unidad = Unidad.objects.get(usuario=request.user)
    facturas = Factura.objects.filter(unidad=unidad)
    pagos = Pago.objects.filter(unidad=unidad)

    saldo_pendiente_total = sum(f.saldo_pendiente_bs() for f in facturas if not f.pagada)

    context = {
        'unidad': unidad,
        'facturas': facturas,
        'pagos': pagos,
        'saldo_pendiente_total': saldo_pendiente_total
    }
    return render(request, 'accounts/mi_cuenta.html', context)

@login_required
def lista_gastos(request):
    gastos = Gasto.objects.all()
    context = {
        'gastos': gastos
    }
    return render(request, 'core/lista_gastos.html', context)

@login_required
def actualizar_tasa_api(request):
    try:
        # Hacer la solicitud a la API oficial
        response = requests.get('https://ve.dolarapi.com/v1/dolares/oficial')
        data = response.json()

        # Obtener el precio del dólar oficial (ahora está en 'promedio')
        tasa = data['promedio']

        # Actualizar o crear la configuración general
        config, created = ConfiguracionGeneral.objects.get_or_create(
            pk=1,  # Solo una instancia
            defaults={'tasa_cambio_actual': tasa}
        )
        config.tasa_cambio_actual = tasa
        config.save()

        return JsonResponse({'status': 'success', 'tasa': tasa})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def actualizar_tasa_manual(request):
    if request.method == 'POST':
        tasa = request.POST.get('tasa')
        try:
            tasa = float(tasa)
            config, created = ConfiguracionGeneral.objects.get_or_create(
                pk=1,
                defaults={'tasa_cambio_actual': tasa}
            )
            config.tasa_cambio_actual = tasa
            config.save()
            messages.success(request, f'Tasa actualizada a {tasa}.')
            return redirect('actualizar_tasa_manual')
        except ValueError:
            messages.error(request, 'Por favor, ingresa un número válido.')
    else:
        config = ConfiguracionGeneral.objects.first()
        tasa_actual = config.tasa_cambio_actual if config else 0

    return render(request, 'core/actualizar_tasa.html', {'tasa_actual': tasa_actual})

@login_required
def lista_cuotas_especiales(request):
    cuotas = CuotaEspecial.objects.all()
    context = {
        'cuotas': cuotas
    }
    return render(request, 'core/lista_cuotas_especiales.html', context)

@login_required
def crear_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save()
            messages.success(request, f'Gasto "{gasto.descripcion}" creado exitosamente.')
            return redirect('crear_gasto')
    else:
        form = GastoForm()

    return render(request, 'core/crear_gasto.html', {'form': form})

@login_required
def mis_facturas(request):
    try:
        unidad = Unidad.objects.get(usuario=request.user)
    except Unidad.DoesNotExist:
        messages.error(request, "No tienes una unidad asociada.")
        return redirect('home')

    facturas = Factura.objects.filter(unidad=unidad).order_by('-fecha_emision')  # ← Agregamos el ordenamiento

    context = {
        'facturas': facturas
    }

    return render(request, 'core/mis_facturas.html', context)

@login_required
def editar_gasto(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Gasto "{gasto.descripcion}" actualizado exitosamente.')
            return redirect('lista_gastos')
    else:
        form = GastoForm(instance=gasto)

    return render(request, 'core/editar_gasto.html', {'form': form})

@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save()
            messages.success(request, f'Pago de "{pago.monto_pagado_bs} Bs" registrado exitosamente.')
            return redirect('crear_pago')
    else:
        form = PagoForm()

    return render(request, 'core/crear_pago.html', {'form': form})

@login_required
def crear_cuota_especial(request):
    if request.method == 'POST':
        form = CuotaEspecialForm(request.POST)
        if form.is_valid():
            cuota = form.save()
            messages.success(request, f'Cuota especial "{cuota.descripcion}" creada exitosamente.')
            return redirect('crear_cuota_especial')
    else:
        form = CuotaEspecialForm()

    return render(request, 'core/crear_cuota_especial.html', {'form': form})

@login_required
def ver_pagos_propietario(request):
    try:
        unidad = Unidad.objects.get(usuario=request.user)
    except Unidad.DoesNotExist:
        messages.error(request, "No tienes una unidad asociada.")
        return redirect('home')

    pagos = Pago.objects.filter(unidad=unidad).order_by('-fecha_pago')

    context = {
        'pagos': pagos
    }
    return render(request, 'core/ver_pagos_propietario.html', context)

@login_required
def ver_saldos_pendientes(request):
    try:
        unidad = Unidad.objects.get(usuario=request.user)
    except Unidad.DoesNotExist:
        messages.error(request, "No tienes una unidad asociada.")
        return redirect('home')

    facturas = Factura.objects.filter(unidad=unidad, pagada=False).order_by('-fecha_emision')

    saldo_pendiente_total = sum(f.saldo_pendiente_bs() for f in facturas)

    context = {
        'facturas': facturas,
        'saldo_pendiente_total': saldo_pendiente_total
    }
    return render(request, 'core/ver_saldos_pendientes.html', context)

login_required
def enviar_estado_cuenta(request):
    try:
        unidad = Unidad.objects.get(usuario=request.user)
    except Unidad.DoesNotExist:
        messages.error(request, "No tienes una unidad asociada.")
        return redirect('home')

    facturas = Factura.objects.filter(unidad=unidad, pagada=False).order_by('-fecha_emision')

    saldo_pendiente_total = sum(f.saldo_pendiente_bs() for f in facturas)

    # Enviar correo electrónico
    asunto = f'Estado de Cuenta - {unidad.nombre}'
    mensaje = f'''
    Hola {unidad.propietario},

    Este es tu estado de cuenta:

    Unidad: {unidad.nombre}
    Propietario: {unidad.propietario}
    Inquilino: {unidad.inquilino}

    Saldo Pendiente Total: {saldo_pendiente_total} Bs

    Facturas Pendientes:
    '''
    for f in facturas:
        mensaje += f'- {f.fecha_emision}: {f.monto_total_bs_fecha_emision} Bs ({f.monto_total_usd} USD)\n'

    mensaje += f'''

    Saludos,
    CondominioApp
    '''

    try:
        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,  # Remitente (debe estar configurado en settings.py)
            [unidad.email],  # Destinatario
            fail_silently=False,
        )
        messages.success(request, f'Estado de cuenta enviado a {unidad.email}.')
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {str(e)}')

    return redirect('mi_cuenta')


@login_required
def enviar_estado_cuenta_telegram(request):
    try:
        unidad = Unidad.objects.get(usuario=request.user)
    except Unidad.DoesNotExist:
        messages.error(request, "No tienes una unidad asociada.")
        return redirect('home')

    facturas = Factura.objects.filter(unidad=unidad, pagada=False).order_by('-fecha_emision')

    saldo_pendiente_total = sum(f.saldo_pendiente_bs() for f in facturas)

    # Enviar mensaje de Telegram
    bot_token = settings.TELEGRAM_BOT_TOKEN  # Debe estar configurado en settings.py
    chat_id = unidad.usuario.telegram_chat_id  # Debe estar guardado en el modelo User

    mensaje = f'''
    Hola {unidad.propietario},

    Este es tu estado de cuenta:

    Unidad: {unidad.nombre}
    Propietario: {unidad.propietario}
    Inquilino: {unidad.inquilino}

    Saldo Pendiente Total: {saldo_pendiente_total} Bs

    Facturas Pendientes:
    '''
    for f in facturas:
        mensaje += f'- {f.fecha_emision}: {f.monto_total_bs_fecha_emision} Bs ({f.monto_total_usd} USD)\n'

    mensaje += f'''

    Saludos,
    CondominioApp
    '''

    try:
        bot = telegram.Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=mensaje)
        messages.success(request, f'Estado de cuenta enviado por Telegram.')
    except Exception as e:
        messages.error(request, f'Error al enviar el mensaje de Telegram: {str(e)}')

    return redirect('mi_cuenta')

@login_required
def generar_factura_pdf(request, id):
    try:
        unidad = Unidad.objects.get(usuario=request.user)
    except Unidad.DoesNotExist:
        messages.error(request, "No tienes una unidad asociada.")
        return redirect('home')

    factura = Factura.objects.get(id=id, unidad=unidad)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Factura #{factura.id}")
    p.drawString(100, 780, f"Unidad: {unidad.nombre}")
    p.drawString(100, 760, f"Propietario: {unidad.propietario}")
    p.drawString(100, 740, f"Monto: {factura.monto_total_usd} USD / {factura.monto_total_bs_fecha_emision} Bs")
    p.showPage()
    p.save()

    return response