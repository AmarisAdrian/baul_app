from django import forms    
from app.cliente.models import ClienteModel

class ClienteFacturacionForm(forms.ModelForm):
    class Meta:
        model = ClienteModel
        fields = [
            'id', 
            'documento',
            'nombre',
            'apellido',       
            'direccion', 
            'email',
            'telefono', 
            #'fecha_ingreso',          
        ]
        labels = {
            'id':'Id', 
            'documento':'Documento ', 
            'nombre':'nombre', 
            'apellido':'apellido',        
            'direccion':'direccion',  
            'email':'email',  
            'telefono':'telefono',  
            #'fecha_ingreso':'descuento',           
        }
        widgets = {
            'id':forms.NumberInput(attrs={'class': 'form-control border border-2' }),
            'documento': forms.NumberInput(attrs={'class': 'form-control border border-2','readonly':'true'}),     
            'nombre':forms.TextInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
            'direccion':forms.TextInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
            'email':forms.TextInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
            'telefono':forms.NumberInput(attrs={'class': 'form-control border border-2','readonly':'true'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = ClienteModel
        fields = [
            'id', 
            'documento',
            'nombre',
            'apellido',       
            'direccion', 
            'email',
            'telefono',          
        ]
        labels = {
            'id':'Id', 
            'documento':'Documento ', 
            'nombre':'nombre', 
            'apellido':'apellido',        
            'direccion':'direccion',  
            'email':'email',  
            'telefono':'telefono',            
        }
        widgets = {
            'id':forms.NumberInput(attrs={'class': 'form-control border border-2' }),
            'documento': forms.NumberInput(attrs={'class': 'form-control border border-2'}),     
            'nombre':forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'direccion':forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'email':forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'telefono':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
        }

class ClienteFormUpdate(forms.ModelForm):
    class Meta:
        model = ClienteModel
        fields = [
            'id', 
            'documento',
            'nombre',
            'apellido',       
            'direccion', 
            'email',
            'telefono',          
        ]
        labels = {
            'id':'Id', 
            'documento':'Documento ', 
            'nombre':'nombre', 
            'apellido':'apellido',        
            'direccion':'direccion',  
            'email':'email',  
            'telefono':'telefono',            
        }
        widgets = {
            'id':forms.NumberInput(attrs={'class': 'form-control border border-2' }),
            'documento': forms.NumberInput(attrs={'class': 'form-control border border-2'}),     
            'nombre':forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'direccion':forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'email':forms.TextInput(attrs={'class': 'form-control border border-2'}),
            'telefono':forms.NumberInput(attrs={'class': 'form-control border border-2'}),
        }