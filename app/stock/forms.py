from django import forms    
from app.stock.models import StockModel

class StockForm(forms.ModelForm):
    class Meta:
        model = StockModel
        fields = [
            'id', 
            'id_producto',
            'cantidad',
            'precio_unitario',       
            'valor', 
            'valor_venta', 
            'descuento',          
            'valor_descuento',
            'motivo_traslado', 
        ]
        labels = {
            'id':'Id', 
            'id_producto':'Producto ', 
            'cantidad':'cantidad', 
            'precio_unitario':'precio unitario',        
            'valor':'valor',  
            'valor_venta':'valor venta',  
            'descuento':'descuento',           
            'valor_descuento':'valor descuento', 
            'motivo_traslado':'Motivo de traslado ',  
        }
        widgets = {
            'id':forms.NumberInput(attrs={'class': 'form-control border border-2' }),
            'id_producto': forms.Select(attrs={'class': 'form-control border border-2'}),     
            'cantidad':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'valor':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'valor_venta':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'descuento':forms.NumberInput(attrs={'class': 'form-control border border-2'}),   
            'valor_descuento':forms.NumberInput(attrs={'class': 'form-control border-2','readonly':'true'}),
            'motivo_traslado':forms.Textarea(attrs={'class': 'form-control border border-2'}),
        }