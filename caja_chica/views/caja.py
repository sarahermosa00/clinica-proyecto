from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.utils import timezone
from decimal import Decimal
from compartido.templatetags.custom_filters import formato_guaranies


#Models
from ..models import MovimientoCajaChica, SaldoDiarioCajaChica

from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font  
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Formularios
from ..forms import MovimientoCajaChicaForm, SaldoDiarioCajaChicaForm

class ListaMovimientosCajaChica(LoginRequiredMixin, generic.ListView):
    template_name = 'clinica/caja/lista_movimientos.html'

    def get(self, request):
        # Obtener la fecha del parámetro GET o usar la fecha de hoy por defecto
        fecha_str = request.GET.get('fecha')
        if fecha_str:
            fecha = timezone.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        else:
            fecha = timezone.localtime().date()

        # Crear o recuperar el saldo diario para la fecha seleccionada
        saldo_diario, creado = SaldoDiarioCajaChica.objects.get_or_create(fecha=fecha)
        
        # Calcular saldo inicial del día si es el primer registro
        if creado:
            saldo_anterior = SaldoDiarioCajaChica.objects.filter(fecha__lt=fecha).first()
            saldo_diario.saldo_inicial = saldo_anterior.saldo_final if saldo_anterior else 0
            saldo_diario.save()

        # Filtrar los movimientos por la fecha seleccionada
        movimientos = MovimientoCajaChica.objects.filter(fecha=fecha)

        # Calcular el saldo final después de actualizar o agregar movimientos
        saldo_diario.calcular_saldo_final()

        context = {
            'movimientos': movimientos,
            'saldo_diario': saldo_diario,
            'form': MovimientoCajaChicaForm() if not saldo_diario.cerrado else None,  # Solo permite registros si no está cerrada
            'fecha': fecha,  # Pasar la fecha seleccionada al contexto para mostrar en el formulario,
            'caja_cerrada': saldo_diario.cerrado,  # Indica si la caja está cerrada
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = MovimientoCajaChicaForm(request.POST)
        if form.is_valid():
            movimiento = form.save()
            # Recalcular saldo del día al agregar nuevo movimiento
            saldo_diario = SaldoDiarioCajaChica.objects.get(fecha=movimiento.fecha)
            saldo_diario.calcular_saldo_final()
            return redirect('caja_chica:lista_movimientos')
        return self.get(request)

class CrearSaldoDiario(LoginRequiredMixin, generic.CreateView):
    template_name = 'clinica/caja/crear_saldo.html'

    def get(self, request):
        form = SaldoDiarioCajaChicaForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SaldoDiarioCajaChicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('caja_chica:lista_movimientos')
        return render(request, self.template_name, {'form': form})


class CerrarCaja(LoginRequiredMixin, generic.View):
    template_name = 'clinica/caja/cerrar_caja.html'

    def get(self, request):
        fecha = timezone.localtime().date()
        saldo_diario = SaldoDiarioCajaChica.objects.filter(fecha=fecha).first()
        if not saldo_diario:
            messages.error(request, "No hay saldo registrado para el día actual.")
            return redirect('caja_chica:lista_movimientos')
        if saldo_diario.cerrado:
            messages.warning(request, "La caja ya ha sido cerrada para el día de hoy.")
            return redirect('caja_chica:lista_movimientos')

        context = {
            'saldo_diario': saldo_diario,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        fecha = timezone.localtime().date()
        saldo_diario = SaldoDiarioCajaChica.objects.filter(fecha=fecha).first()
        if not saldo_diario:
            messages.error(request, "No hay saldo registrado para el día actual.")
            return redirect('caja_chica:lista_movimientos')

        if saldo_diario.cerrado:
            messages.warning(request, "La caja ya ha sido cerrada para el día de hoy.")
            return redirect('caja_chica:lista_movimientos')

        # Obtener el saldo físico ingresado por el usuario
        saldo_fisico = request.POST.get('saldo_fisico')
        try:
            saldo_fisico = float(saldo_fisico)
        except ValueError:
            messages.error(request, "Por favor, ingresa un monto válido.")
            return redirect('caja_chica:cerrar_caja')

        # Cerrar la caja
        saldo_diario.cerrar_caja(saldo_fisico)

        # Si hay diferencia, ajustar el saldo inicial del día siguiente
        if saldo_diario.diferencia != 0:
            fecha_siguiente = fecha + timezone.timedelta(days=1)
            saldo_siguiente, _ = SaldoDiarioCajaChica.objects.get_or_create(fecha=fecha_siguiente)
            saldo_siguiente.saldo_inicial += saldo_diario.diferencia
            saldo_siguiente.save()

        messages.success(request, "La caja ha sido cerrada correctamente.")
        return redirect('caja_chica:lista_movimientos')

# def gestionar_caja(request):
#     if request.method == "POST":
#         fecha = timezone.localtime().date()
#         saldo_diario = SaldoDiarioCajaChica.objects.filter(fecha=fecha).first()

#         if not saldo_diario:
#             messages.error(request, "No hay saldo diario registrado para el día actual.")
#             return redirect('caja_chica:lista_movimientos')

#         # Si la caja está cerrada, permitir abrirla
#         # if saldo_diario.cerrado:
#         #     saldo_diario.abrir_caja()
#         #     messages.success(request, "Caja abierta correctamente.")
#         # else:
#         #     # Cerrar la caja y manejar la diferencia
#         #     saldo_fisico = request.POST.get('saldo_fisico')
#         #     try:
#         #         saldo_fisico = Decimal(saldo_fisico)
#         #     except (TypeError, ValueError):
#         #         messages.error(request, "Saldo físico no válido.")
#         #         return redirect('caja_chica:lista_movimientos')

#         #     saldo_diario.cerrar_caja(saldo_fisico)

#         #     # Notificar al usuario sobre la diferencia
#         #     if saldo_diario.diferencia != 0:
#         #         messages.warning(
#         #             request, 
#         #             f"Caja cerrada con una diferencia."
#         #             "El saldo inicial del día siguiente ha sido ajustado."
#         #         )
#         #     else:
#         #         messages.success(request, "Caja cerrada correctamente.")
#         if saldo_diario.cerrado:
#             # Reabrir la caja y ajustar el saldo si se proporciona un nuevo saldo físico
#             nuevo_saldo_fisico = request.POST.get('saldo_fisico')
#             if nuevo_saldo_fisico:
#                 saldo_diario.abrir_caja(nuevo_saldo_fisico)
#                 nuevo_saldo_fisico_formateado = formato_guaranies(nuevo_saldo_fisico)
#                 messages.success(
#                     request,
#                     f"Caja reabierta y ajustada con un saldo físico de {nuevo_saldo_fisico_formateado}."
#                 )
#             else:
#                 saldo_diario.abrir_caja()
#                 messages.success(request, "Caja reabierta correctamente.")

#         else:
#             # Cerrar la caja
#             saldo_fisico = request.POST.get('saldo_fisico')
#             try:
#                 saldo_fisico = Decimal(saldo_fisico)
#             except (TypeError, ValueError):
#                 messages.error(request, "Saldo físico no válido.")
#                 return redirect('caja_chica:lista_movimientos')

#             saldo_diario.cerrar_caja(saldo_fisico)
#             # Notificar al usuario sobre la diferencia
#             if saldo_diario.diferencia != 0:
#                 messages.warning(
#                     request, 
#                     f"Caja cerrada con una diferencia."
#                 )
#             else:
#                 messages.success(request, "Caja cerrada correctamente.")

#     return redirect('caja_chica:lista_movimientos')

def gestionar_caja(request):
    if request.method == "POST":
        fecha = timezone.localtime().date()
        saldo_diario = SaldoDiarioCajaChica.objects.filter(fecha=fecha).first()

        if not saldo_diario:
            messages.error(request, "No hay saldo diario registrado para el día actual.")
            return redirect('caja_chica:lista_movimientos')

        if saldo_diario.cerrado:
            # Reabrir la caja
            nuevo_saldo_fisico = request.POST.get('saldo_fisico')
            if nuevo_saldo_fisico:
                try:
                    nuevo_saldo_fisico = Decimal(nuevo_saldo_fisico)
                except (TypeError, ValueError):
                    messages.error(request, "Saldo físico no válido.")
                    return redirect('caja_chica:lista_movimientos')

                saldo_diario.abrir_caja(nuevo_saldo_fisico)

                # Actualizar saldo inicial del día siguiente
                fecha_siguiente = fecha + timezone.timedelta(days=1)
                saldo_siguiente, creado = SaldoDiarioCajaChica.objects.get_or_create(fecha=fecha_siguiente)
                saldo_siguiente.saldo_inicial = saldo_diario.saldo_final
                saldo_siguiente.save()

                messages.success(
                    request,
                    f"Caja reabierta y ajustada con un saldo físico de {formato_guaranies(nuevo_saldo_fisico)}"
                )
            else:
                saldo_diario.abrir_caja()
                messages.success(request, "Caja reabierta correctamente.")
        else:
            # Cerrar la caja
            saldo_fisico = request.POST.get('saldo_fisico')
            try:
                saldo_fisico = Decimal(saldo_fisico)
            except (TypeError, ValueError):
                messages.error(request, "Saldo físico no válido.")
                return redirect('caja_chica:lista_movimientos')

            saldo_diario.cerrar_caja(saldo_fisico)

            # Actualizar saldo inicial del día siguiente
            # fecha_siguiente = fecha + timezone.timedelta(days=1)
            # saldo_siguiente, creado = SaldoDiarioCajaChica.objects.get_or_create(fecha=fecha_siguiente)
            # saldo_siguiente.saldo_inicial = saldo_diario.saldo_final
            # saldo_siguiente.save()

            if saldo_diario.diferencia != 0:
                messages.warning(
                    request,
                    f"Caja cerrada con una diferencia de {formato_guaranies(saldo_diario.diferencia)} "
                    "El saldo inicial del día siguiente ha sido ajustado automáticamente."
                )
            else:
                messages.success(request, "Caja cerrada correctamente.")

    return redirect('caja_chica:lista_movimientos')


def exportar_pdf(request):
    # Crear el objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="movimientos_caja.pdf"'

    # Crear el objeto canvas
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Movimientos de Caja Chica")
    
    saldo = SaldoDiarioCajaChica.objects.get(fecha=timezone.localtime().date())

    # documento_formateado = f"{int(emp['documento']):,}".replace(",", ".")

    def formato_monto(monto):
        return f"{int(monto):,}".replace(",", ".")

    # Fecha de generación del reporte
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 80, f"Fecha de generación: {timezone.localtime().strftime('%d/%m/%Y')}")
    p.drawString(50, height - 100, "Saldo Inicial: " + formato_monto(saldo.saldo_inicial)+" Gs")
    p.drawString(50, height - 120, "Saldo Final: " + formato_monto(saldo.saldo_final)+" Gs")


    # Cabecera de la tabla
    y = height - 140
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Fecha")
    p.drawString(150, y, "Concepto")
    p.drawString(300, y, "Entrada")
    p.drawString(400, y, "Salida")
    y -= 20

    # Obtener movimientos y llenar la tabla
    movimientos = MovimientoCajaChica.objects.filter(fecha=timezone.localtime().date())
    p.setFont("Helvetica", 10)
    
    total_entrada = 0
    total_salida = 0

    for movimiento in movimientos:
        # Fecha, Concepto, Tipo
        p.drawString(50, y, movimiento.fecha.strftime('%d %b. %Y'))
        p.drawString(150, y, movimiento.concepto)

        # Entrada o Salida según el tipo de movimiento
        if movimiento.tipo == 'entrada':
            p.drawString(300, y, formato_monto(movimiento.monto) + " Gs")
            p.drawString(400, y, "0")
            total_entrada += movimiento.monto
        else:
            p.drawString(300, y, "0")
            p.drawString(400, y, formato_monto(movimiento.monto) +" Gs")
            total_salida += movimiento.monto
        
        y -= 20  # Mover la posición verticalmente para la siguiente fila

        # Salto de página si se llena la hoja
        if y < 50:
            p.showPage()
            y = height - 50

    # Totales
    p.setFont("Helvetica-Bold", 12)
    p.drawString(200, y - 20, "Totales:")
    p.drawString(300, y - 20, formato_monto(total_entrada) + " Gs")
    p.drawString(400, y - 20, formato_monto(total_salida) + " Gs")

    # Finalizar el PDF
    p.showPage()
    p.save()

    return response