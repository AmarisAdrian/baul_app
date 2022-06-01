from re import I
from django.shortcuts import render
from app.producto.form import ProductoForm,UploadFileForm,ProductoFormUpdate,GuardarImagenProductoForm
from app.producto.models import ProductoModel,ImagenProductoModel
from app.stock.models import StockModel
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from app.producto.resources import ProductoResource
from app.config.message import Message
from sweetify.views import SweetifySuccessMixin
from django.shortcuts import redirect
from tablib import Dataset 
from django.core import serializers
from app.config.views import RegistrarLog
from app.config.models import NotificacionModel
from django.db.models import Q
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
#import django_excel as excel


#se coloca la ruta donde está el index del empleado
class index(LoginRequiredMixin,ListView): 
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ProductoModel
    template_name = 'producto/producto.html'
    context_object_name = 'producto'

class CreateProducto(LoginRequiredMixin,CreateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ProductoModel
    template_name = 'producto/crear-producto.html'
    success_url = reverse_lazy('producto:producto')
    form_class = ProductoForm
    #LAS SIGUIENTES FUNCIONES  NO SON COMPLETAMENTE NECESARIAS SOLO ES PARA PERSONALIZAR#
    def get_context_data(self, *args, **kwargs):      
        context = super(CreateProducto, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET) 
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(self.request.POST)
        modulo = "producto/CreateProducto/post"
        try:
            if form.is_valid():
                sw = form.save(commit=False)
                sw.save()
                Message.SuccessMessage(self.request,'El producto se ha guardado exitosamente')                         
            else:
                Message.ErrorMessage(self.request,'Ha ocurrido un error al guardar el producto ')              
                RegistrarLog(modulo, 'Ha ocurrido un error'+ str(form.errors) ,self.request.POST) 
                return render(request, 'producto/crear-producto.html', {'form': form})
            return HttpResponseRedirect(self.get_success_url())              
        except Exception as ex:
            RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex) ,self.request.POST)
            Message.ErrorMessage(self.request,ex)
            return redirect('producto:producto')


class UpdateProducto(LoginRequiredMixin,SweetifySuccessMixin,UpdateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ProductoModel
    template_name = 'producto/editar-producto.html'
    success_url = reverse_lazy('producto:producto')
    form_class = ProductoFormUpdate
    success_message = 'Producto actualizado exitosamente'
    #LAS SIGUIENTES FUNCIONES  NO SON COMPLETAMENTE NECESARIAS SOLO ES PARA VALIDAR SI ESTA HACIENDO EL POST#
    def get_context_data(self, **kwargs):      
        context = super(UpdateProducto, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        producto = self.model.objects.get(id=pk)       
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET) 
        return context
        
    def post(self, request, *args, **kwargs):
        modulo = "producto/UpdateProducto/post"
        self.object = self.get_object
        id = kwargs['pk']
        producto = self.model.objects.get(id=id)
        form = self.form_class(self.request.POST,instance=producto)    
        try:
            if form.is_valid():
                sw = form.save(commit=False)
                sw.save()
                Message.SuccessMessage(self.request,'El producto se ha actualizado exitosamente')        
            else:
                Message.ErrorMessage(self.request,'ha ocurrido un error al actualizar producto')
                RegistrarLog(modulo, 'Ha ocurrido un error'+ str(form.errors) ,self.request.POST) 
                return render(request, 'producto/editar-producto.html', {'form': form})
            return redirect('producto:producto')
        except Exception as ex:
            RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex) ,self.request.POST)
            Message.ErrorMessage(self.request,ex)
            return redirect('producto:producto')
    

class DeleteProducto(LoginRequiredMixin,SweetifySuccessMixin,DeleteView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ProductoModel
    context_object_name = 'producto'
    template_name = 'producto/eliminar-producto.html'
    success_url = reverse_lazy('producto:producto')
    form_class = ProductoForm
    success_message = 'Producto eliminado exitosamente'

def ImportarProducto(request):
    try:
        if request.method == 'POST':
            productos = request.FILES['importar_producto']  
            producto_resource = ProductoResource()  
            dataset = Dataset()  
            imported_data = dataset.load(productos.read())
            result = producto_resource.import_data(dataset, dry_run=True) 
            if not result.has_errors():  
                producto_resource.import_data(dataset, dry_run=False) 
                Message.SuccessMessage(request,'Archivo de producto importado exitosamente')
                return redirect('producto:producto')
            else:
                Message.ErrorMessage(request,'Archivo de producto no pudo ser importado')
                return redirect('producto:producto')
    except Exception as ex:
            Message.ErrorMessage(request,ex.Message)
            return redirect('producto:producto')
    return render(request,'producto/importar-producto.html')

@login_required
def ConsultarProducto(request):
    model = ProductoModel
    context_object_name = 'producto'
    logger = logging.getLogger()
    modulo = "PRODUCTO/CONSULTARPRODUCTO"
    requested = []
    try:
        if request.method == 'POST':
            referencia = request.POST.get('referencia_producto')
            if referencia != '':
                producto = model.objects.filter(referencia=referencia).exists()               
                if producto:
                    dato_producto = model.objects.get(referencia=referencia)  
                    stock = StockModel.objects.filter(id_producto = dato_producto.id).exists()
                    if stock: 
                        dato_stock = StockModel.objects.filter(id_producto = dato_producto.id).latest()
                        responseData = {
                            'status': 'ok',
                            'code': 200,
                            'msj': 'Producto encontrado',
                            'datos': [{
                                'id':dato_producto.id,
                                'descripcion':dato_producto.descripcion,
                                'detalle_producto':dato_producto.detalle_producto,
                                'valor_venta':dato_stock.valor_venta,
                                'descuento':dato_stock.descuento,
                                'cantidad':dato_stock.cantidad ,
                                'valor_descuento':dato_stock.valor_descuento 
                                
                            }]
                        }                  
                    else:
                        responseData = {
                            'status': 'error',
                            'code': 200,
                            'msj': 'El producto se encuentra registrado pero no ha sido cargado en el inventario'
                        }
                else:
                    responseData = {
                        'status': 'error',
                        'code': 200,
                        'msj': 'Producto no encontrado'
                    } 
            else:
                responseData = {
                    'status': 'error',
                    'code': 200,
                    'msj': 'Campo de referencia no puede ir vacio'
                }

            return JsonResponse(responseData,safe=False)
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: '+ str(ex)
        }
        RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex) ,requested)
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
    return JsonResponse(responseData,safe=False)

@login_required
def NotificacionStockProducto():
    model = ProductoModel
    context_object_name = 'producto'
    logger = logging.getLogger()
    modulo = "PRODUCTO/NOTIFICACIONSTOCKPRODUCTO"
    model_notificacion = NotificacionModel
    try:
        stock = StockModel.objects.filter(cantidad__lte=2).exists()             
        if stock:
            dato_stock = StockModel.objects.filter(cantidad__lte=2).order_by('-id')
            for i in dato_stock:
                notificacion = NotificacionModel.objects.filter(referencia= i.id).exists()
                if notificacion == False:
                    model_notificacion = NotificacionModel()
                    model_notificacion.referencia = i
                    model_notificacion.modulo = 'Stock producto'
                    model_notificacion.descripcion = 'Producto:'+ str(i.id_producto)+' tiene: ' + str(i.cantidad) +' en stock'
                    model_notificacion.estado = False
                    model_notificacion.save()   
                    save = True
                    if save:
                        RegistrarLog(modulo, 'Notificacion registrada','En stock ') 
                    else:
                        RegistrarLog(modulo, 'Notificacion no pudo ser registrada','En stock')      
    except Exception as ex:
        RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex) ,'NULL')
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))


@login_required
def ConsultarProductoInventario(request):
    model = ProductoModel
    context_object_name = 'producto'
    logger = logging.getLogger()
    modulo = "PRODUCTO/ConsultarProductoInventario"
    requested = []
    try:
        if request.method == 'POST':
            referencia = request.POST.get('TxtBuscarProducto')
            if referencia != '': 
                producto = model.objects.filter(Q(codigo=referencia) | Q(referencia=referencia)).exists()           
                if producto:
                    dato_producto = model.objects.filter(Q(codigo=referencia) | Q(referencia=referencia)) 
                    stock = StockModel.objects.filter(id_producto = dato_producto[0].id).exists()
                    if stock:
                        stock = StockModel.objects.filter(id_producto = dato_producto[0].id).order_by('-fecha_movimiento')[:1]
                        responseData = {
                            'status': 'success',
                            'code': 200,
                            'msj': 'Producto encontrado',
                            'datos': {
                                'id':stock[0].id,
                                'id_producto':dato_producto[0].id,
                                'descripcion':dato_producto[0].descripcion,
                                'cantidad':stock[0].cantidad                            
                            }
                        }
                    else:
                        responseData = {
                            'status': 'ok',
                            'code': 200,
                            'msj': 'Producto no cargado al stock'
                        }                  
                else:
                    responseData = {
                        'status': 'Error',
                        'code': 200,
                        'msj': 'El producto no existe'
                        }
            else:
                responseData = {
                    'status': 'Error',
                    'code': 200,
                    'msj': 'Campo de referencia no puede ir vacio'
                } 
        else:
            responseData = {
                'status': 'Error',
                'code': 200,
                'msj': 'Error de validacion'
            }
        return JsonResponse(responseData,safe=False)
    except Exception as ex:
        responseData = {
            'status': 'Error',
            'code': 500,
            'msj': 'Informacion no procesada: '+ str(ex)
        }
        RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex) ,requested)
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
    return JsonResponse(responseData,safe=False)


@login_required
def ConsultarProductoModal(request,pk):
    model = ProductoModel
    modulo = 'Producto/ConsultarImagenProducto'
    logger = logging.getLogger()
    try:
        if pk is not None or pk != "":
            producto = ProductoModel.objects.filter(id = pk).exists()
            if producto :
                producto = ProductoModel.objects.get(id = pk)
                responseData = {
                    'status': 'success',
                    'code': 200,
                    'msj': 'Producto encontrado',
                    'producto': {
                        'id':producto.id,
                        'descripcion':producto.descripcion,
                        'detalle':producto.detalle_producto              
                    }
                }    
            else:
                responseData = {
                    'status': 'error',
                    'code': 500,
                    'msj': 'Error de validacion'
                }
        else:
            responseData = {
                'status': 'error',
                'code': 500,
                'msj': 'Error de validacion'
            }
        return render(request, 'producto/modal-producto.html', {'dato': responseData})
    except Exception as ex:      
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: ' + str(ex)
        }
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
        RegistrarLog(modulo,str(ex),'NULL')
        return JsonResponse(responseData,safe=False)

@login_required
def CreateImagenProducto(request):
    model = ImagenProductoModel
    modulo = 'Producto/CreateImagenProducto'
    logger = logging.getLogger()
    success_url = reverse_lazy('producto:producto')
    try:
        if request.method == "POST":
            producto = request.POST.get('producto')
            descripcion = request.POST.get('descripcion-imagen')
            imagen = request.FILES['file']
            if producto != "" or descripcion != "" or imagen !="":
                producto = ProductoModel.objects.get(pk=producto)
                model = ImagenProductoModel()
                model.producto = producto
                model.descripcion = descripcion
                model.adjunto = imagen
                model.save()
                sw = True
                if sw:
                    Message.SuccessMessage(request,'Imagen guardada exitosamente') 
                else:
                    Message.ErrorMessage(request,'No se pudo guardar la imagen')
            else:
                Message.ErrorMessage(request,'Ha ocurrido un error de validacion')
        return redirect('producto:producto')
    except Exception as ex:      
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: ' + str(ex)
        }
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
        RegistrarLog(modulo,str(ex),'NULL')
        return JsonResponse(responseData,safe=False)
   
class indexCatalogo(LoginRequiredMixin,ListView): 
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ImagenProductoModel
    template_name = 'producto/catalogo.html'
    context_object_name = 'catalogo'