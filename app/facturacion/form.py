from django import forms    
from app.facturacion.models import FacturacionModel, DetalleFacturacionModel

class FacturacionForm(forms.ModelForm):
    class Meta:
        model = FacturacionModel
        fields = [
            'id',
            'numero_factura',
            'cliente',
            'subtotal',
            'total',
            'envio',
        ]
        labels = {
            'id':'Id',
            'numero_factura':'Numero Factura',
            'cliente' : 'Cliente',
            'subtotal' : 'Subtotal',
            'total' : 'Total',
            'envio' : 'Envio',
        }
        widgets = {
            'id':forms.Select(attrs={'class': 'form-control border border-2' }),
            'numero_factura': forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'cliente':forms.Select(attrs={'class': 'form-control border border-2'}),
            'subtotal':forms.NumberInput(attrs={'class': 'form-control border border-2', 'readonly':'true'}),
            'total':forms.NumberInput(attrs={'class': 'form-control border border-2', 'readonly':'true'}),
            'envio':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
        }
        
class DetalleFacturacionForm(forms.ModelForm):
    class Meta:
        model = DetalleFacturacionModel
        fields = [
            'id',
            'id_producto',
            'cantidad',
            'valor',
            'id_factura',
        ]
        labels = {
            'id' : 'Id',
            'id_producto' : 'Producto',
            'cantidad' : 'Cantidad',
            'valor' : 'Valor',
            'id_factura' : 'Factura',
        }
        widgets = {
            'id':forms.NumberInput(attrs={'class': 'form-control border border-2' }),
            'id_producto':forms.TextInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
            'cantidad':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'valor':forms.NumberInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
            'id_factura':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
        }


