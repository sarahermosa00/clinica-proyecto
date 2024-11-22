from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.utils import timezone

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

        # Filtrar los movimientos por la fecha seleccionada
        movimientos = MovimientoCajaChica.objects.filter(fecha=fecha)
        saldo_diario, creado = SaldoDiarioCajaChica.objects.get_or_create(fecha=fecha)
        
        # Calcular saldo inicial del día si es el primer registro
        if creado:
            saldo_anterior = SaldoDiarioCajaChica.objects.filter(fecha__lt=fecha).first()
            saldo_diario.saldo_inicial = saldo_anterior.saldo_final if saldo_anterior else 0
            saldo_diario.save()

        # Calcular el saldo final después de actualizar o agregar movimientos
        saldo_diario.calcular_saldo_final()

        context = {
            'movimientos': movimientos,
            'saldo_diario': saldo_diario,
            'form': MovimientoCajaChicaForm(),
            'fecha': fecha,  # Pasar la fecha seleccionada al contexto para mostrar en el formulario
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

# Generar XLSX   
# def exportar_pago_xlsx(request, pk):
#     # Obtener el pago de salario por su ID
#     pago = PagoSalario.objects.get(pk=pk)
#     empleados_salarios = []
#     for empleado in pago.empleados.all():
#         salario_total = empleado.salario_base + empleado.bonificaciones - empleado.deducciones
#         empleados_salarios.append({
#             'empleado': empleado,
#             'salario_total': salario_total
#         })
    
#     # Crear archivo Excel
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Hoja1"
    
#     bold_font = Font(bold=True) 

#     # Formatear encabezados con celdas combinadas
#     # Título general en las celdas B1 a E1
#     ws.merge_cells('A1:G2')
#     ws['A1'] = "PLANILLA DE PAGOS DE SALARIO"
#     ws["A1"].font = bold_font   
#     ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    
#     empresa = "Fundacion Años Dorados"

#     # Empresa en las celdas B2 a E3
#     ws.merge_cells('A3:G3')
#     ws['A3'] = "Empresa: " + empresa
#     ws["A3"].font = bold_font
#     ws['A3'].alignment = Alignment(horizontal="center", vertical="center")

#     # Datos generales
#     fecha_actual = datetime.now().strftime("%Y-%m-%d")
#     mes_anho = datetime.now().strftime("%b%y")  # Ejemplo: Oct24
#     numero = f"{mes_anho}"
    
#     # Encabezado general
#     ws["A5"] = "Número:"
#     ws["A5"].font = bold_font
#     ws["B5"] = "Fecha de acreditación:"
#     ws["B5"].font = bold_font
#     ws["C5"] = "Tipo de Liquidacion:"
#     ws["C5"].font = bold_font
#     ws["D5"] = "Nota:"
#     ws["D5"].font = bold_font
#     ws["E5"] = "Total:"
#     ws["E5"].font = bold_font
#     ws["F5"] = "Moneda"
#     ws["F5"].font = bold_font
#     ws["G5"] = "Cuenta Débito"
#     ws["G5"].font = bold_font

#     # Datos en fila 6
#     ws["A6"] = numero
#     ws["B6"] = fecha_actual
#     ws["C6"] = "Salario"
#     ws["D6"] = ""  # Nota vacía

#     total_salarios = sum([emp['salario_total'] for emp in empleados_salarios])
    
#     ws["E6"] = total_salarios
#     ws["F6"] = "PYG"
#     ws["G6"] = ""  # Cuenta Débito vacía
    
#     # Encabezados de la lista de empleados
#     ws["A7"] = "Tipo Documento"
#     ws["A7"].font = bold_font
#     ws["B7"] = "Nro. Documento"
#     ws["B7"].font = bold_font
#     ws["C7"] = "Nombre"
#     ws["C7"].font = bold_font
#     ws["D7"] = "Monto"
#     ws["D7"].font = bold_font
#     ws["E7"] = "Cuenta"
#     ws["E7"].font = bold_font

#     # Llenar la lista de empleados
#     row = 8
#     for empleado in empleados_salarios:
#         ws[f"A{row}"] = "CI"  # Tipo de documento
#         ws[f"B{row}"] = empleado['empleado'].documento
#         ws[f"C{row}"] = empleado['empleado'].nombre
#         ws[f"D{row}"] = empleado['salario_total']
#         ws[f"E{row}"] = empleado['empleado'].cuenta_bancaria
#         row += 1

#     # Ajustar tamaño de las columnas
#     for col in range(2, 7):
#         ws.column_dimensions[get_column_letter(col)].width = 20

#     # Preparar la respuesta HTTP con el archivo Excel
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = f'attachment; filename="pago_salarios_{pago.id}.xlsx"'
    
#     # Guardar el archivo en la respuesta
#     wb.save(response)
    
#     return response


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