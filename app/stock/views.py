from django.shortcuts import render
from app.stock.forms import StockForm
from app.stock.models import StockModel
from app.producto.models import ProductoModel
from app.producto.views import NotificacionStockProducto
from app.producto.form import ProductoForm,ProductoFormUpdateStock
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from app.config.message import Message
from sweetify.views import SweetifySuccessMixin
from django.shortcuts import redirect
from app.config.views import RegistrarLog
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import logging
import json

class Stock(LoginRequiredMixin,ListView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = StockModel
    template_name = 'stock/stock.html'
    datos = None
    logger = logging.getLogger()
    modulo = "STOCK/STOCK" 
    def post(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                referencia = request.POST.get('referencia')
                producto = ProductoModel.objects.filter(referencia=referencia).exists()
                if producto:
                    self.datos = ProductoModel.objects.get(referencia=referencia)
                    stock = StockModel.objects.filter(id_producto=self.datos.id).exists()
                    if stock:
                        mov = StockModel.objects.filter(id_producto=self.datos.id)                         
                        stock = []  
                        for detalle in mov:
                            stock.append({
                                'fecha_movimiento':str(detalle.fecha_movimiento),
                                'precio_unitario':detalle.precio_unitario,
                                'valor_venta':detalle.valor_venta,
                                'descuento':detalle.descuento,
                                'cantidad':detalle.cantidad,
                                'valor':detalle.valor,
                                'valor_descuento':detalle.valor_descuento,
                                'motivo':detalle.motivo_traslado 
                            })
                        responseData = {
                            'status': 'ok',
                            'code': 200,
                            'msj': 'Producto cargado',
                            'stock':  stock                        
                            }
                    else:
                        responseData = {
                            'status': 'error',
                            'code': 200,
                            'msj': 'Producto no relacionado en el stock'
                        }
                else:
                    responseData = {
                            'status': 'error',
                            'code': 200,
                            'msj': 'El Producto no se encuentra registrado'
                    }
                return JsonResponse(responseData,safe=False)
        except Exception as ex:     
            responseData = {
                'status': 'error',
                'code': 500,
                'msj': 'Informacion no procesada'
            }
            logger.exception('Excepcion controlada: ' + str(ex))
            logger.error('Excepcion controlada: ' + str(ex))
            RegistrarLog(modulo,str(ex),'NULL')
        return JsonResponse(responseData,safe=False)



class MovimientoStock(LoginRequiredMixin,CreateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = StockModel
    template_name = 'stock/movimiento-stock.html'
    form_class = StockForm
    context_object_name = 'stock'
   #LAS SIGUIENTES FUNCIONES  NO SON COMPLETAMENTE NECESARIAS SOLO ES PARA PERSONALIZAR#
    def get_context_data(self, *args, **kwargs):
        context = super(MovimientoStock, self).get_context_data(**kwargs)
        id_producto = self.kwargs.get('id_producto',0)
        producto = ProductoModel.objects.filter(id=id_producto)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(self.request.POST)
        try:
            if form.is_valid():
                sw = form.save(commit=False)
                sw.save()
                Message.SuccessMessage(self.request,'Movimiento de stock satisfactorio')
                return HttpResponseRedirect(self.get_success_url())
            else:
                Message.ErrorMessage(self.request,'No se pudo mover el stock ')
                return redirect('producto:producto')
        except Exception as ex:
            Message.ErrorMessage(self.request,ex)
            return redirect('producto:producto')

class UpdateStock(LoginRequiredMixin,UpdateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = ProductoModel
    second_model = StockModel
    template_name = 'stock/movimiento-stock.html'
    form_class = StockForm
    second_form_class = ProductoFormUpdateStock
    def get_context_data(self, *args, **kwargs):
        context = super(UpdateStock, self).get_context_data(**kwargs)
        id_producto = self.kwargs.get('pk',0)
        producto = ProductoModel.objects.filter(id=id_producto).exists()
        if producto:
            if 'form' not in context:
                context['form'] = self.form_class(self.request.GET)
            if 'form2' not in context:
                context['form2'] = self.second_form_class(self.request.GET)
                context['id_producto'] = id_producto
            return context
        else:
            Message.SuccessMessage(self.request,'El producto no existe ')
            return redirect('producto:producto')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id = self.kwargs.get('pk',0)
        producto = ProductoModel.objects.get(id=id)
        if producto:
            form = self.form_class(self.request.POST)
            form2 = self.second_form_class(self.request.POST,instance=producto)
            try:
                if form.is_valid() and form2.is_valid():
                    sw = form.save(commit=False)
                    sw.producto = form2.save()
                    sw.save()
                    Message.SuccessMessage(self.request,'Stock actualizado exitosamente')
                    return redirect('producto:producto')
                else:
                    Message.ErrorMessage(self.request,'Stock no pudo actualizarse')
                    return redirect('producto:producto')
            except Exception as ex:
                Message.ErrorMessage(self.request,ex)
                return redirect('producto:producto')
        else:
            Message.SuccessMessage(self.request,'El producto no existe ')
            return redirect('producto:producto')

    
class ComparacionStock(LoginRequiredMixin,CreateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = StockModel
    second_model = ProductoModel
    template_name = 'stock/modal-comparacion.html'
    context_object_name = 'stock'
    form_class = StockForm
    

def StockFactura(id_producto, cantidad):
    model = StockModel
    producto_model = ProductoModel
    stock_actualizado = False
    modulo = "Stock/StockFactura"
    requested = []
    logger = logging.getLogger()
    cantidad_activa = 0
    try:
        print("ID PRODUCTO" + str(id_producto))
        if id_producto != '':
            producto = producto_model.objects.filter(id = id_producto).exists()
            if producto:
                producto_stock = model.objects.filter(id_producto = id_producto).exists()
                if producto_stock:
                    id_producto_cantidad  = model.objects.filter(id_producto=id_producto).latest()
                    cantidad_activa = int(id_producto_cantidad.cantidad) - int(cantidad)
                    dato_stock  = StockModel()
                    dato_stock.id_producto = id_producto_cantidad.id_producto
                    dato_stock.precio_unitario = id_producto_cantidad.precio_unitario
                    dato_stock.valor = id_producto_cantidad.valor
                    dato_stock.valor_venta = id_producto_cantidad.valor_venta
                    dato_stock.descuento = id_producto_cantidad.descuento
                    dato_stock.cantidad = cantidad_activa
                    dato_stock.valor_descuento = id_producto_cantidad.valor_descuento
                    dato_stock.motivo_traslado = 'Compra realizada'
                    dato_stock.save()
                    stock_actualizado = True
                    if stock_actualizado:
                        RegistrarLog(modulo, 'Stock actualizado',requested)
                    else:
                        requested.append(id_producto,dato_stock.precio_unitario,dato_stock.valor,dato_stock.valor_venta,dato_stock.descuento,dato_stock.cantidad,dato_stock.motivo_traslado)
                        RegistrarLog(modulo, 'Stock no pudo actualizarse',requested)
            else:
                RegistrarLog(modulo, 'Producto no existe',id_producto)   
        else:
            RegistrarLog(modulo, 'Validacion de producto vacio','NULL')
        return  stock_actualizado
    except Exception as ex:
        RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex) ,requested)
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
    return  stock_actualizado

class Inventario(LoginRequiredMixin,ListView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = StockModel
    template_name = 'inventario/inventario.html'
    context_object_name = 'inventario'

class Inventariar(LoginRequiredMixin,ListView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = StockModel
    template_name = 'inventario/inventariar.html'
    context_object_name = 'inventariar'
    
@login_required
def CruzarInventario(request):
    model = StockModel
    second_model = ProductoModel
    logger = logging.getLogger()
    modulo = "STOCK/CRUZARINVENTARIO"
    requested = []
    try:
        if request.method == 'POST':
            producto = second_model.objects.exists()
            if producto:
                producto = second_model.objects.all()
                for producto in producto :
                    stock = model.objects.filter(id_producto = producto.id).exists()
                    if stock == False:
                        dato_stock  = StockModel()
                        dato_stock.id_producto = producto
                        dato_stock.precio_unitario = producto.precio_unitario
                        dato_stock.valor = producto.valor
                        dato_stock.valor_venta = producto.valor_venta
                        dato_stock.descuento = producto.descuento
                        dato_stock.cantidad = producto.cantidad
                        dato_stock.valor_descuento = producto.valor_descuento
                        dato_stock.motivo_traslado = 'Stock Cargado Automaticamente'
                        dato_stock.save()
                        stock_actualizado = True
                        if stock_actualizado:
                            RegistrarLog(modulo, 'Stock actualizado automaticamente',requested)
                            responseData = {
                                'status': 'success',
                                'code': 200,
                                'msj': 'Stock actualizado automaticamente'
                            }
                        else:
                            requested.append(producto.id,dato_stock.precio_unitario,dato_stock.valor,dato_stock.valor_venta,dato_stock.descuento,dato_stock.cantidad,dato_stock.motivo_traslado)
                            RegistrarLog(modulo, 'Stock no pudo actualizarse automaticamente',requested)
                            responseData = {
                                'status': 'error',
                                'code': 200,
                                'msj': 'El Stock no se pudo actualizar'
                            }
                    else:
                        responseData = {
                            'status': 'error',
                            'code': 200,
                            'msj': 'Hay productos que se encuentran registrados'
                        }
            else:
                RegistrarLog(modulo, 'La tabla no tiene productos registrados',requested)
                responseData = {
                    'status': 'error',
                    'code': 200,
                    'msj': 'La tabla no tiene productos registrados'
                }
        else:
            RegistrarLog(modulo, 'Error de validación',requested)
            responseData = {
                'status': 'error',
                'code': 200,
                'msj': 'Error de validación'
            }
        return JsonResponse(responseData,safe=False)                                          
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': str(ex)
        }
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
        RegistrarLog(modulo,str(ex),'NULL')
        return JsonResponse(responseData,safe=False)

@login_required
def RelacionarInventario(request):
    model = StockModel
    second_model = ProductoModel
    logger = logging.getLogger()
    modulo = "STOCK/RelacionarInventario"
    requested = []
    msj = ""
    try:
        if request.method == 'POST':
            inventario = request.POST.getlist('inventario') 
            datos = json.loads(inventario[0])
            for key in datos.values():
                if key['cantidad'] != key['iteracion']:
                    msj = 'El producto '+ str(key['descripcion']) + ' fue contado:'+ str(key['iteracion']) +' veces, pero en stock tiene ' + str(key['cantidad']) + '. las cantidades no concuerdan'
                    descripcion = key['descripcion'] 
                    id_producto = key['id_producto']
                    status = 'dispaer'
                    requested.append({
                        'msj':msj,
                        'descripcion': descripcion,
                        'id_producto': id_producto,
                        'status':status
                    })            
                if key['cantidad'] == key['iteracion']:
                    msj = 'El producto' + str(key['descripcion']) + ' fue contado:'+ str(key['iteracion']) +' veces, pero en stock tiene ' + str(key['cantidad']) + '. las cantidades concuerdan'
                    descripcion = key['descripcion'] 
                    id_producto = key['id_producto']
                    status = 'ok'
                    requested.append({
                        'msj':msj,
                        'descripcion': descripcion,
                        'id_producto': id_producto,
                        'status':status
                    })
            responseData = {
                'status': 'success',
                'code': 200,
                'msj': 'Inventario escrutado',
                'resultado': requested
            }
        else:
            responseData = {
                'status': 'error',
                'code': 500,
                'msj': 'Error de validacion'
            }
        return JsonResponse(responseData,safe=False)
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': str(ex)
        }
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
        RegistrarLog(modulo,str(ex),'NULL')
        return JsonResponse(responseData,safe=False)


            
        
