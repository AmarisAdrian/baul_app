from django.shortcuts import render
from app.cliente.models import ClienteModel
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from app.config.message import Message
from sweetify.views import SweetifySuccessMixin
from django.shortcuts import redirect
from app.cliente.forms import ClienteFacturacionForm , ClienteForm , ClienteFormUpdate
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from app.config.views import RegistrarLog

# Create your views here.
@login_required
def ConsultarCliente(request):
    model = ClienteModel
    form_class = ClienteFacturacionForm
    context_object_name = 'cliente'
    try:
        if request.method == 'POST':
            documento = request.POST.get('documento')
            if documento != '':
                cliente = model.objects.filter(documento=documento).exists()
                if cliente:
                    dato_cliente = ClienteModel.objects.get(documento=documento)  
                    responseData = {
                        'status': 'ok',
                        'code': 200,
                        'msj': 'Cliente encontrado',
                        'datos': [{
                            'nombre':dato_cliente.nombre,
                            'apellido': dato_cliente.apellido,
                            'direccion':dato_cliente.direccion,
                            'telefono': dato_cliente.telefono,
                            'email': dato_cliente.email
                        }]
                    }
                else:
                    responseData = {
                        'status': 'error',
                        'code': 200,
                        'msj': 'Cliente no encontrado'
                    } 
            else:
                 responseData = {
                        'status': 'error',
                        'code': 200,
                        'msj': 'Campo de documento no puede ir vacio'
                    } 
            return JsonResponse(responseData,safe=False)
    except Exception as ex:
            Message.ErrorMessage(request,'Informacion no procesada')
            return redirect('facturacion:crear-facturacion')

class index(LoginRequiredMixin,ListView): 
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ClienteModel
    template_name = 'cliente/cliente.html'
    context_object_name = 'cliente'

class CreateCliente(LoginRequiredMixin,CreateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ClienteModel
    template_name = 'cliente/crear-cliente.html'
    success_url = reverse_lazy('cliente:cliente')
    form_class = ClienteForm
    #LAS SIGUIENTES FUNCIONES  NO SON COMPLETAMENTE NECESARIAS SOLO ES PARA PERSONALIZAR#
    def get_context_data(self, *args, **kwargs):      
        context = super(CreateCliente, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET) 
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(self.request.POST)
        modulo = "cliente/CreateCliente/post"
        try:
            if form.is_valid():
                sw = form.save(commit=False)
                sw.save()
                Message.SuccessMessage(self.request,'El cliente se ha guardado exitosamente')                    
            else:
                Message.ErrorMessage(self.request,'Ha ocurrido un error')
                RegistrarLog(modulo, 'Ha ocurrido un error'+ str(form.errors) ,self.request.POST) 
                return render(request, 'cliente/crear-cliente.html', {'form': form})
            return HttpResponseRedirect(self.get_success_url())  
        except Exception as ex:
            RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex) ,self.request.POST)
            Message.ErrorMessage(self.request,ex)
            return redirect('cliente:cliente')

class UpdateCliente(LoginRequiredMixin,SweetifySuccessMixin,UpdateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ClienteModel
    template_name = 'cliente/editar-cliente.html'
    success_url = reverse_lazy('cliente:cliente')
    form_class = ClienteFormUpdate
    success_message = 'Cliente actualizado exitosamente'
    #LAS SIGUIENTES FUNCIONES  NO SON COMPLETAMENTE NECESARIAS SOLO ES PARA VALIDAR SI ESTA HACIENDO EL POST#
    def get_context_data(self, **kwargs):      
        context = super(UpdateCliente, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        cliente = self.model.objects.get(id=pk)       
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET) 
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        cliente = self.model.objects.get(id=id)
        form = self.form_class(self.request.POST,instance=cliente)  
        modulo = "cliente/UpdateCliente/post"  
        try:
            if form.is_valid():
                sw = form.save(commit=False)
                sw.save()
                Message.SuccessMessage(self.request,'El cliente se ha actualizado exitosamente') 
                        
            else:
                Message.ErrorMessage(self.request,'Los datos ya existen.Por favor intente con nuevos datos')
                RegistrarLog(modulo, 'Ha ocurrido un error'+ str(form.errors) ,self.request.POST) 
                return render(request, 'cliente/editar-cliente.html', {'form': form})
            return HttpResponseRedirect(self.get_success_url())   
        except Exception as ex:
            RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex) ,self.request.POST)
            Message.ErrorMessage(self.request,ex)
            return redirect('cliente:cliente')

class DeleteCliente(LoginRequiredMixin,SweetifySuccessMixin,DeleteView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ClienteModel
    context_object_name = 'cliente'
    template_name = 'cliente/eliminar-cliente.html'
    success_url = reverse_lazy('cliente:cliente')
    form_class = ClienteForm
    success_message = 'Cliente eliminado exitosamente'