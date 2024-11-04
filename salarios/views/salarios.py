from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Empleado, PagoSalario
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
from ..forms import FormularioPagoSalario


class PantallaSalarios(LoginRequiredMixin, generic.TemplateView):
    template_name = 'clinica/salarios/pantalla_salarios.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        # Obtener mes y año de la solicitud GET
        mes = self.request.GET.get('mes')
        anho = self.request.GET.get('anho')

        # Filtrar los pagos por mes y año si están presentes
        if mes and anho:
            salarios = PagoSalario.objects.filter(fecha_pago__month=mes, fecha_pago__year=anho)
        else:
            salarios = PagoSalario.objects.all()

        # Agregar los pagos filtrados al contexto
        contexto['salarios'] = salarios.order_by('-fecha_pago')

        # Añadir el mes y año actual al contexto para los filtros
        contexto['mes_actual'] = datetime.now().month
        contexto['anho_actual'] = datetime.now().year

        # Crear una lista de meses del 1 al 12
        contexto['meses'] = range(1, 13)

        return contexto

class GenerarPagoSalario(LoginRequiredMixin, generic.CreateView):
    model = PagoSalario
    form_class = FormularioPagoSalario
    template_name = 'clinica/salarios/generar_pago.html'

    def form_valid(self, form):
        pago_salario = form.save(commit=False)  # No guarda todavía
        pago_salario.fecha_pago = datetime.now()
    
        # Asignamos los empleados seleccionados
        empleados = form.cleaned_data['empleados']  # Obtenemos los empleados seleccionados
        
        # Calculamos el salario total para todos los empleados
        salario_total = 0
        for empleado in empleados:
            salario_base = empleado.salario_base
            bonificaciones = empleado.bonificaciones
            deducciones = empleado.deducciones

            # Calcula el salario del empleado
            salario_empleado = salario_base + bonificaciones - deducciones
            salario_total += salario_empleado

        # Asignamos el salario total calculado antes de guardar
        pago_salario.salario_total = salario_total
        pago_salario.save()  # Ahora guardamos con el salario total

        # Asignamos los empleados a la relación ManyToMany
        pago_salario.empleados.set(empleados)

        messages.success(self.request, 'Pago de salario generado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('salarios:pantalla_salarios')
    

class ListarPagosSalarios(LoginRequiredMixin, generic.ListView):
    model = PagoSalario
    template_name = 'clinica/salarios/lista_pagos.html'
    context_object_name = 'pagos'

    def get_queryset(self):
        mes = self.request.GET.get('mes', None)
        anho = self.request.GET.get('anho', None)
        if mes and anho:
            return PagoSalario.objects.filter(fecha_pago__month=mes, fecha_pago__year=anho)
        return PagoSalario.objects.all()

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['mes_actual'] = datetime.now().month
        contexto['anho_actual'] = datetime.now().year
        return contexto

class DetallePagoSalario(LoginRequiredMixin, generic.DetailView):
    model = PagoSalario
    template_name = 'clinica/salarios/detalle_pago_salario.html'
    context_object_name = 'pago'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        # Obtener los empleados relacionados al pago de salario
        empleados = self.object.empleados.all()
        # Calcular el salario total de cada empleado
        empleados_salarios = []
        for empleado in empleados:
            salario_total = empleado.salario_base + empleado.bonificaciones - empleado.deducciones
            empleados_salarios.append({
                'empleado': empleado,
                'salario_total': salario_total
            })
        # Pasar los empleados y sus salarios totales al contexto
        contexto['empleados_salarios'] = empleados_salarios
        return contexto

# Generar XLSX   
def exportar_pago_xlsx(request, pk):
    # Obtener el pago de salario por su ID
    pago = PagoSalario.objects.get(pk=pk)
    empleados_salarios = []
    for empleado in pago.empleados.all():
        salario_total = empleado.salario_base + empleado.bonificaciones - empleado.deducciones
        empleados_salarios.append({
            'empleado': empleado,
            'salario_total': salario_total
        })
    
    # Crear archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Hoja1"
    
    bold_font = Font(bold=True) 

    # Formatear encabezados con celdas combinadas
    # Título general en las celdas B1 a E1
    ws.merge_cells('A1:G2')
    ws['A1'] = "PLANILLA DE PAGOS DE SALARIO"
    ws["A1"].font = bold_font   
    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    
    empresa = "Fundacion Años Dorados"

    # Empresa en las celdas B2 a E3
    ws.merge_cells('A3:G3')
    ws['A3'] = "Empresa: " + empresa
    ws["A3"].font = bold_font
    ws['A3'].alignment = Alignment(horizontal="center", vertical="center")

    # Datos generales
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    mes_anho = datetime.now().strftime("%b%y")  # Ejemplo: Oct24
    numero = f"{mes_anho}"
    
    # Encabezado general
    ws["A5"] = "Número:"
    ws["A5"].font = bold_font
    ws["B5"] = "Fecha de acreditación:"
    ws["B5"].font = bold_font
    ws["C5"] = "Tipo de Liquidacion:"
    ws["C5"].font = bold_font
    ws["D5"] = "Nota:"
    ws["D5"].font = bold_font
    ws["E5"] = "Total:"
    ws["E5"].font = bold_font
    ws["F5"] = "Moneda"
    ws["F5"].font = bold_font
    ws["G5"] = "Cuenta Débito"
    ws["G5"].font = bold_font

    # Datos en fila 6
    ws["A6"] = numero
    ws["B6"] = fecha_actual
    ws["C6"] = "Salario"
    ws["D6"] = ""  # Nota vacía

    total_salarios = sum([emp['salario_total'] for emp in empleados_salarios])
    
    ws["E6"] = total_salarios
    ws["F6"] = "PYG"
    ws["G6"] = ""  # Cuenta Débito vacía
    
    # Encabezados de la lista de empleados
    ws["A7"] = "Tipo Documento"
    ws["A7"].font = bold_font
    ws["B7"] = "Nro. Documento"
    ws["B7"].font = bold_font
    ws["C7"] = "Nombre"
    ws["C7"].font = bold_font
    ws["D7"] = "Monto"
    ws["D7"].font = bold_font
    ws["E7"] = "Cuenta"
    ws["E7"].font = bold_font

    # Llenar la lista de empleados
    row = 8
    for empleado in empleados_salarios:
        ws[f"A{row}"] = "CI"  # Tipo de documento
        ws[f"B{row}"] = empleado['empleado'].documento
        ws[f"C{row}"] = empleado['empleado'].nombre
        ws[f"D{row}"] = empleado['salario_total']
        ws[f"E{row}"] = empleado['empleado'].cuenta_bancaria
        row += 1

    # Ajustar tamaño de las columnas
    for col in range(2, 7):
        ws.column_dimensions[get_column_letter(col)].width = 20

    # Preparar la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="pago_salarios_{pago.id}.xlsx"'
    
    # Guardar el archivo en la respuesta
    wb.save(response)
    
    return response


def exportar_pago_pdf(request, pk):
    # Obtener el pago de salario por su ID
    pago = PagoSalario.objects.get(pk=pk)
    empleados_salarios = []
    for empleado in pago.empleados.all():
        salario_total = empleado.salario_base + empleado.bonificaciones - empleado.deducciones
        empleados_salarios.append({
            'documento': empleado.documento,
            'nombre': empleado.nombre,
            'salario_total': salario_total,
            'cuenta_bancaria': empleado.cuenta_bancaria or 'N/A'
        })

    # Configuración del archivo PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Configurar el encabezado y la información de la empresa
    empresa = "Fundacion Años Dorados"
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    titulo = "PLANILLA DE PAGOS DE SALARIOS"
    encabezado_altura = 4 * cm

    # Dibujar título, empresa y fecha centrados en la parte superior
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - encabezado_altura, titulo)
    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, height - encabezado_altura - 1 * cm, f"Empresa: {empresa}")
    p.drawCentredString(width / 2, height - encabezado_altura - 2 * cm, f"Fecha de acreditación: {fecha_actual}")

    # Total de salarios
    total_salarios = sum(emp['salario_total'] for emp in empleados_salarios)

    # Crear los datos de la tabla de empleados
    data = [["Nro. Documento", "Nombre", "Monto", "Cuenta"]]
    for emp in empleados_salarios:
        # Formatear el documento y el salario total con puntos como separadores de miles
        documento_formateado = f"{int(emp['documento']):,}".replace(",", ".")
        salario_formateado = f"{emp['salario_total']:,}".replace(",", ".")
        
        data.append([
            documento_formateado,
            emp['nombre'],
            salario_formateado,
            emp['cuenta_bancaria']
        ])

    # Crear la tabla y agregar estilo
    table = Table(data, colWidths=[4 * cm, 6 * cm, 4 * cm, 4 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    # Calcular la posición vertical para la tabla inmediatamente después del encabezado
    y_position = height - encabezado_altura - 6 * cm  # Ajustar para que esté debajo del encabezado

    # Dibujar la tabla en la posición especificada
    table.wrapOn(p, width, height)
    table.drawOn(p, 2 * cm, y_position)

    # Mostrar el total de pagos inmediatamente debajo de la tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawRightString(width - 2 * cm, y_position - (len(data) * 0.5 * cm) - 1 * cm, f"Total Pagado: {total_salarios:,} PYG")

    # Finalizar el archivo PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    
    # Respuesta HTTP para descargar el PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pago_salarios_{pago.id}.pdf"'
    return response