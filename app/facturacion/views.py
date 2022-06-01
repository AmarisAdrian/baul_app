from django.shortcuts import render
from app.facturacion.form import FacturacionForm, DetalleFacturacionForm
from app.facturacion.models import FacturacionModel, DetalleFacturacionModel
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.producto.models import ProductoModel
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect,  JsonResponse
from django.contrib import messages
from app.config.message import Message
from sweetify.views import SweetifySuccessMixin
from django.shortcuts import redirect
from tablib import Dataset 
from app.cliente.forms import ClienteFacturacionForm
from app.cliente.models import ClienteModel
from app.cliente.forms import ClienteFacturacionForm
from app.cotizacion.models import CotizacionModel,DetalleCotizacionModel
from django.views.decorators.csrf import csrf_exempt
from app.config.views import ConsultarConsecutivoFactura
from datetime import date,datetime
from app.config.models import LogModel
from app.stock.views import StockFactura
from app.config.views import RegistrarLog
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json
from django.utils.safestring import SafeString
import logging
from app.reporte.views import ImprimirCotizacion,ImprimirFactura


class index(LoginRequiredMixin,ListView): 
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = FacturacionModel
    template_name = 'facturacion/facturacion.html'
    context_object_name = 'facturacion'

class CreateFacturacion(LoginRequiredMixin,CreateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    form_cliente = ClienteFacturacionForm
    model = FacturacionModel
    second_model = DetalleFacturacionModel
    template_name = 'facturacion/crear-facturacion.html'
    success_url = reverse_lazy('facturacion:facturacion')
    form_class = FacturacionForm
    second_form_class = DetalleFacturacionForm
    
    #LAS SIGUIENTES FUNCIONES  NO SON COMPLETAMENTE NECESARIAS SOLO ES PARA PERSONALIZAR#
    def get_context_data(self, *args, **kwargs):      
        context = super(CreateFacturacion, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET) 
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET) 
        if 'form3' not in context:
            context['form3'] = self.form_cliente(self.request.GET) 
        return context

@login_required
def GenerarFacturacion(request):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = FacturacionModel
    second_model = DetalleFacturacionModel
    cliente_model = ClienteModel
    producto_model = ProductoModel
    main_factura = False
    second_factura = False
    logger = logging.getLogger()
    modulo = "Facturacion/GenerarFacturacion"
    requested = []
    try:
        if request.method == 'POST':
            carrito = request.POST.getlist('factura') 
            datos = json.loads(carrito[0])
            if datos :
                consecutivo = ConsultarConsecutivoFactura()
                cliente = ClienteModel.objects.filter(documento=datos['0']['id_cliente']).exists()
                if cliente:
                    cliente_factura = cliente_model.objects.get(documento=datos['0']['id_cliente'])
                    model = model()
                    model.numero_factura = consecutivo
                    model.cliente = cliente_factura
                    model.subtotal = datos['0']['id_subtotal']
                    model.total = datos['0']['id_total']
                    model.envio = datos['0']['envio']
                    model.fecha_ingreso = datetime.now()            
                    model.save()
                    id = model       
                    main_factura = True
                    if main_factura:       
                        for key in datos.values():
                            producto = producto_model.objects.filter(referencia=key['referencia_producto']).exists() 
                            if producto:
                                second_model = DetalleFacturacionModel()
                                imp = ImprimirFactura()
                                dato_producto = producto_model.objects.get(referencia=key['referencia_producto']) 
                                if  key['TxtDescuento'] ==0:
                                    key['id_valor'] = key['TxtDescuento']                         
                                second_model.id_factura = model
                                second_model.id_producto = dato_producto
                                second_model.cantidad = key['id_cantidad']  
                                second_model.valor = key['id_valor']
                                second_model.save()
                                second_factura = True
                                imp.get(pk = id.id)
                                try:
                                    mov_stock = StockFactura(dato_producto.id, second_model.cantidad )
                                    if mov_stock:
                                        RegistrarLog(modulo, 'Movimiento de stock exitoso','NULL')
                                    else:
                                        requested.append([dato_producto.id, second_model.cantidad])
                                        RegistrarLog(modulo, 'No se pudo mover stock',requested)
                                except Exception as ex:
                                    RegistrarLog(modulo, 'Excepcion controlada: ' + str(ex),requested)
                            else:
                                responseData = {
                                'status': 'error',
                                'code': 201,
                                'msj': 'Producto no encontrado'
                            }
                        if second_factura:                            
                            responseData = {
                                'status': 'success',
                                'code': 200,
                                'msj': 'Factura generada'
                            }
                        else:
                            responseData = {
                                'status': 'error',
                                'code': 200,
                                'msj': 'Factura no generada'
                            }
                    else:
                        responseData = {
                            'status': 'error',
                            'code': 200,
                            'msj': 'Factura principal no pudo ser guardada'
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
                    'msj': 'Datos de JSON no leido exitosamente'
                }
        else:
            responseData = {
                'status': 'error',
                'code': 200,
                'msj': 'Parametros enviados no validados'
            }
        return JsonResponse(responseData,safe=False)
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: ' + str(ex)
        }
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
        return JsonResponse(responseData,safe=False)


@login_required
def FacturarCotizacion(request):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = CotizacionModel
    second_model = DetalleCotizacionModel
    factura_model = FacturacionModel
    detalle_factura_model = DetalleFacturacionModel
    producto_model = ProductoModel
    main_factura = False
    second_factura = False
    logger = logging.getLogger()
    modulo = "Facturacion/FacturarCotizacion"
    requested = []
    try:
        if request.method == 'POST':
            id_cotizacion = request.POST.get('id') 
            if id_cotizacion :
                consecutivo = ConsultarConsecutivoFactura()
                cotizacion = CotizacionModel.objects.filter(id = id_cotizacion).exists()
                if cotizacion:
                    cotizacion = CotizacionModel.objects.get(id = id_cotizacion)
                    if cotizacion.estado == 1:
                        model = FacturacionModel()                    
                        model.numero_factura = consecutivo
                        model.cliente = cotizacion.cliente
                        model.subtotal = cotizacion.subtotal
                        model.total = cotizacion.total
                        model.envio = cotizacion.envio
                        model.fecha_ingreso = datetime.now()     
                        model.save()   
                        id = model 
                        main_factura = True
                        if main_factura:    
                            for key in DetalleCotizacionModel.objects.filter(id_cotizacion=id_cotizacion):
                                producto = producto_model.objects.filter(id=key.id_producto.id).exists() 
                                if producto:
                                    second_model = DetalleFacturacionModel()
                                    imp = ImprimirCotizacion()
                                    dato_producto = producto_model.objects.get(id=key.id_producto.id)                 
                                    second_model.id_factura = model
                                    second_model.id_producto = dato_producto
                                    second_model.cantidad = key.cantidad 
                                    second_model.valor = key.valor
                                    second_model.save()
                                    cotizacion = CotizacionModel.objects.get(id = id_cotizacion)
                                    cotizacion.estado = 2
                                    cotizacion.save()
                                    second_factura = True
                                    imp.get(pk = id.id)
                                    try:
                                        mov_stock = StockFactura(dato_producto.id, second_model.cantidad )            
                                        if mov_stock:
                                            RegistrarLog(modulo, 'Movimiento de stock exitoso','NULL')
                                        else:
                                            requested.append([dato_producto.id, second_model.cantidad])
                                            RegistrarLog(modulo, 'No se pudo mover stock',requested)
                                    except Exception as ex:
                                        RegistrarLog("FacturarCotizacion/mov-stock", 'Excepcion controlada: ' + str(ex),requested)
                                else:
                                    responseData = {
                                    'status': 'error',
                                    'code': 201,
                                    'msj': 'Producto no encontrado'
                                }
                            if second_factura:                            
                                responseData = {
                                    'status': 'success',
                                    'code': 200,
                                    'msj': 'Factura generada'
                                }
                            else:
                                responseData = {
                                    'status': 'error',
                                    'code': 200,
                                    'msj': 'Factura no generada'
                                }
                        else:
                            responseData = {
                                'status': 'error',
                                'code': 200,
                                'msj': 'Factura principal no pudo ser guardada'
                        }
                    else:
                        responseData = {
                            'status': 'error',
                            'code': 200,
                            'msj': 'La factura ya se encuentra facturada'
                        }
                else:
                    responseData = {
                        'status': 'error',
                        'code': 200,
                        'msj': 'Cotizacion no encontrada'
                    }
            else:
                responseData = {
                    'status': 'error',
                    'code': 200,
                    'msj': 'Datos de JSON no leido exitosamente'
                }
        else:
            responseData = {
                'status': 'error',
                'code': 200,
                'msj': 'Parametros enviados no validados'
            }
        return JsonResponse(responseData,safe=False)
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: ' + str(ex)
        }
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
    return JsonResponse(responseData,safe=False)


@login_required
def ConsultarFactura(request,pk):
    model = FacturacionModel
    second_model = DetalleFacturacionModel
    logger = logging.getLogger()
    modulo = "FACTURACION/CONSULTARFACTURA" 
    context_object_name = 'factura'
    try:
        if pk != "" or pk != None:
            factura = model.objects.filter(id=pk).exists() 
            detalle_factura = second_model.objects.filter(id_factura=pk).exists()
            if factura and detalle_factura:
                factura = model.objects.get(id=pk)
                detalle_factura = second_model.objects.filter(id_factura=pk) 
                detalle_factura_json = []     
                fecha_ingreso = factura.fecha_ingreso.strftime("%Y-%m-%d %H:%M:%S")
                for detalle in detalle_factura:
                    detalle_factura_json.append({
                        'id_factura':pk,
                        'id_producto':detalle.id_producto.descripcion,
                        'cantidad':detalle.cantidad,
                        'valor':detalle.valor,
                        'fecha_ingreso':str(detalle.fecha_ingreso )                  
                    })
                responseData = {
                    'status': 'success',
                    'code': 200,
                    'msj': 'Factura encontrada',
                    'factura': {
                        'id':factura.id,
                        'numero_factura':factura.numero_factura,
                        'cliente':factura.cliente.nombre+' '+factura.cliente.apellido,
                        'subtotal':factura.subtotal,
                        'total':factura.total,
                        'envio':factura.envio,
                        'fecha_ingreso':fecha_ingreso                 
                    },
                  'detalle_factura': detalle_factura_json
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
        return render(request, 'facturacion/modal-facturacion.html', {'dato': responseData})
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

    

