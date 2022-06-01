from django import forms    
from app.producto.models import ProductoModel,ImagenProductoModel

class ProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoModel
        fields = [
            'id', 
            'codigo',
            'descripcion', 
            'detalle_producto', 
            'talla', 
            'precio_unitario',
            'valor', 
            'valor_venta', 
            'descuento', 
            'cantidad',
            'valor_descuento', 
            'id_motivo', 
            'referencia', 
            'pieza',
        ]
        labels = {
            'id':'Id ',
            'codigo':'Codigo producto',
            'descripcion':'Descripcion ',
            'detalle_producto':'Detalle producto',
            'talla':'Talla',
            'precio_unitario':'Precio unitario',
            'valor':'Valor neto',
            'valor_venta':'Valor venta',
            'descuento':'Descuento',
            'cantidad':'cantidad',
            'valor_descuento':'Valor descuento',
            'id_motivo':'Motivo',
            'referencia':'referencia',
            'pieza':'pieza',
        }
        widgets = {
            'id':forms.Select(attrs={'class': 'form-control border border-2' ,'required':'true'}),
            'codigo': forms.NumberInput(attrs={'class': 'form-control border border-2','required':'true'}),
            'descripcion':forms.TextInput(attrs={'class': 'form-control border border-2','required':'true'}),
            'detalle_producto':forms.Textarea(attrs={'class': 'form-control border border-2', 'style': 'height: 80px','required':'true'}),
            'talla': forms.TextInput(attrs={'class': 'form-control border border-2','required':'true'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control border border-2','required':'true'}),
            'valor':forms.NumberInput(attrs={'class': 'form-control border border-2','required':'true'}),
            'valor_venta':forms.NumberInput(attrs={'class': 'form-control border border-2','required':'true'}),
            'descuento':forms.NumberInput(attrs={'class': 'form-control border border-2','required':'true'}),
            'cantidad':forms.NumberInput(attrs={'class': 'form-control border border-2','required':'true'}),
            'valor_descuento':forms.NumberInput(attrs={'class': 'form-control border-2','readonly':'true','required':'true'}),
            'id_motivo':forms.Select(attrs={'class': 'form-control border border-2','required':'true'}),
            'referencia':forms.NumberInput(attrs={'class': 'form-control border-2','required':'true'}),
            'pieza':forms.NumberInput(attrs={'class': 'form-control border-2','required':'true'}),
        }

class ProductoFormUpdate(forms.ModelForm):
    class Meta:
        model = ProductoModel
        fields = [
            'id', 
            'codigo',
            'descripcion', 
            'detalle_producto', 
            'talla', 
            'precio_unitario',
            'valor', 
            'valor_venta', 
            'descuento', 
            'cantidad',
            'valor_descuento', 
            'id_motivo', 
            'referencia', 
            'pieza',
        ]
        labels = {
            'id':'Id ',
            'codigo':'Codigo producto',
            'descripcion':'Descripcion ',
            'detalle_producto':'Detalle producto',
            'talla':'Talla',
            'precio_unitario':'Precio unitario',
            'valor':'Valor neto',
            'valor_venta':'Valor venta',
            'descuento':'Descuento',
            'cantidad':'cantidad',
            'valor_descuento':'Valor descuento',
            'id_motivo':'Motivo',
            'referencia':'referencia',
            'pieza':'pieza',
        }
        widgets = {
            'id':forms.Select(attrs={'class': 'form-control border border-2' }),
            'codigo': forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'descripcion':forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'detalle_producto':forms.Textarea(attrs={'class': 'form-control border border-2', 'style': 'height: 80px'}),
            'talla': forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'valor':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'valor_venta':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'descuento':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'cantidad':forms.NumberInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
            'valor_descuento':forms.NumberInput(attrs={'class': 'form-control border-2','readonly':'true'}),
            'id_motivo':forms.Select(attrs={'class': 'form-control border border-2'}),
            'referencia':forms.NumberInput(attrs={'class': 'form-control border-2'}),
            'pieza':forms.NumberInput(attrs={'class': 'form-control border-2'}),
        }

class ProductoFormUpdateStock(forms.ModelForm):
    class Meta:
        model = ProductoModel
        fields = [
            'id',
            'cantidad',
            'precio_unitario',       
            'valor', 
            'valor_venta', 
            'descuento',          
            'valor_descuento',
        ]
        labels = {
            'id':'Id ',
            'cantidad':'cantidad', 
            'precio_unitario':'precio unitario',        
            'valor':'valor',  
            'valor_venta':'valor venta',  
            'descuento':'descuento',           
            'valor_descuento':'valor descuento', 
            'descripcion':'Motivo de traslado ',  
        }
        widgets = {
            'id':forms.Select(attrs={'class': 'form-control border border-2' }),
            'id_producto': forms.NumberInput(attrs={'class': 'form-control border border-2','readonly':'true'}),     
            'cantidad':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'valor':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'valor_venta':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
            'descuento':forms.NumberInput(attrs={'class': 'form-control border border-2'}),   
            'valor_descuento':forms.NumberInput(attrs={'class': 'form-control border-2','readonly':'true'}),
        }

class UploadFileForm(forms.Form):

    fields = [         
      'importar_producto',
    ]
    widgets = {
        'importar_producto': forms.FileField()       
    }

class GuardarImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenProductoModel
        fields = [
            'producto',
            'descripcion',       
            'adjunto', 
        ]
        labels = {
            'producto':'producto', 
            'descripcion':'descripcion',        
            'adjunto':'adjunto',
        }
        widgets = {
            'producto': forms.NumberInput(attrs={'class': 'form-control d-block'}),     
            'descripcion':forms.Textarea(attrs={'class': 'form-control'}),
            'adjunto': forms.FileInput(attrs={'class': 'btn bg-pollo text-light btn-fill btn-wd'}), 
        }
          