from django.forms import ModelForm, ChoiceField
from django import forms

from .models import *

from factura.models.modelo_proveedor import Proveedor
from factura.models.modelo_objeto import ObjetoFactura


class FormularioProveedor(ModelForm):
    """Se tiene que llamar como la clase de mi modelo de donde quiero hacer el formulario
    django maneja solo el tema de los formularios, solo deberia especificar los que son choices, los demas si se quiere añadirle estilos css 
    
    """

    class Meta:
        model = Proveedor
        fields = '__all__'
    

    """
    en el modelo yo para definir estos campos utilice 
     TIPO_CLIENTE_OPCIONES = [
        ('C', 'Cliente'),
        ('P', 'Proveedor'),
        ('A', 'Ambos')
    ]

    tipo = models.CharField(
        max_length=1,
        choices=TIPO_CLIENTE_OPCIONES,
        default='C',
        verbose_name="Tipo de entidad (Cliente, Proveedor, Ambos)"
    )

    donde los choices tienen un campo especifico, no estaba guardando porque aca estaba 
    proveedor.objects.all()
    y tenia que ser especifico para que sepa donde buscar

    choices=Proveedor.TIPO_CLIENTE_OPCIONES,
    
    
    """
  
        
    estado = ChoiceField(
        choices=Proveedor.ESTADO_OPCIONES,
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'}),
    )
        
    tipo = ChoiceField(
        choices=Proveedor.TIPO_CLIENTE_OPCIONES,
        label='Tipo',
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'})

    )





    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)





class FormularioObjeto(ModelForm):

    class Meta:
        model = ObjetoFactura
        fields = '__all__'

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)