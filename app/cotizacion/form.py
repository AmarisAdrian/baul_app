from django import forms
from app.cotizacion.models import CotizacionModel,DetalleCotizacionModel

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = CotizacionModel
        fields = [
            'id',
            'cliente',
            'subtotal',
            'total',
            'estado',
            'envio',
        ]
        labels = {
            'id':'Id',
            'cliente' : 'Cliente',
            'subtotal' : 'Subtotal',
            'total' : 'Total',
            'estado' : 'Estado',
            'envio' : 'Envio',
        }
        widgets = {
            'id':forms.Select(attrs={'class': 'form-control border border-2' }),
            'cliente':forms.Select(attrs={'class': 'form-control border border-2'}),
            'subtotal':forms.NumberInput(attrs={'class': 'form-control border border-2', 'readonly':'true'}),
            'total':forms.NumberInput(attrs={'class': 'form-control border border-2', 'readonly':'true'}),
            'estado':forms.NumberInput(attrs={'class': 'form-control border border-2', 'readonly':'true'}),
            'envio':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
        }

class DetalleFacturacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacionModel
        fields = [
            'id',
            'id_producto',
            'cantidad',
            'valor',
        ]
        labels = {
            'id' : 'Id',
            'id_producto' : 'Producto',
            'cantidad' : 'Cantidad',
            'valor' : 'Valor',
        }
        widgets = {
            'id':forms.NumberInput(attrs={'class': 'form-control border border-2' }),
            'id_producto':forms.TextInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
            'cantidad':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'valor':forms.NumberInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
        }