from django.shortcuts import render
from django.views.generic import ListView, CreateView
from app.cotizacion.models import CotizacionModel,DetalleCotizacionModel
from app.cliente.models import ClienteModel
from app.producto.models import ProductoModel
from app.config.views import RegistrarLog
from django.http import JsonResponse
from datetime import date,datetime
import logging
import json
from app.reporte.views import ImprimirCotizacion

# Create your views here.
class index(ListView):
    model = CotizacionModel
    template_name = 'cotizacion/cotizacion.html'
    context_object_name = 'cotizacion'

def CrearCotizacion(request):
    model = CotizacionModel
    second_model = DetalleCotizacionModel
    cliente_model = ClienteModel
    producto_model = ProductoModel
    main_factura = False
    second_factura = False
    logger = logging.getLogger()
    modulo = "COTIZACION/CREARCOTIZACION"
    requested = []
    try:
        if request.method == 'POST':
            carrito = request.POST.getlist('cotizacion') 
            datos = json.loads(carrito[0])
            if datos :
                cliente = ClienteModel.objects.filter(documento=datos['0']['id_cliente']).exists()
                if cliente:
                    cliente_cotizacion = cliente_model.objects.get(documento=datos['0']['id_cliente'])
                    model = model()
                    model.cliente = cliente_cotizacion
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
                                second_model = DetalleCotizacionModel()
                                imp = ImprimirCotizacion()
                                dato_producto = producto_model.objects.get(referencia=key['referencia_producto']) 
                                if  key['TxtDescuento'] ==0:
                                    key['id_valor'] = key['TxtDescuento']   
                                second_model.id_cotizacion = id
                                second_model.id_producto = dato_producto
                                second_model.cantidad = key['id_cantidad']  
                                second_model.valor = key['id_valor']
                                second_model.save()
                                second_factura = True
                                RegistrarLog(modulo, 'Cotizacion generada exitosamente','NULL')
                                imp.get(pk = id.id)
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
                                'msj': 'Cotizacion generada',
                                'id' : id.id
                            }
                        else:
                            responseData = {
                                'status': 'error',
                                'code': 200,
                                'msj': 'Cotizacion no generada',  
                            }
                    else:
                        responseData = {
                            'status': 'error',
                            'code': 200,
                            'msj': 'Cotizacion principal no pudo ser guardada'
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

def ConsultarCotizacion(request,pk):
    model = CotizacionModel
    second_model = DetalleCotizacionModel
    logger = logging.getLogger()
    modulo = "FACTURACION/CONSULTARFACTURA" 
    context_object_name = 'factura'
    try:
        if pk != "" or pk != None:
            cotizacion = model.objects.filter(id=pk).exists() 
            detalle_cotizacion = second_model.objects.filter(id_cotizacion=pk).exists()
            if cotizacion and detalle_cotizacion:
                cotizacion = model.objects.get(id=pk)
                detalle_cotizacion = second_model.objects.filter(id_cotizacion=pk) 
                detalle_cotizacion_json = []     
                fecha_ingreso = cotizacion.fecha_ingreso.strftime("%Y-%m-%d %H:%M:%S")
                for detalle in detalle_cotizacion:
                    detalle_cotizacion_json.append({
                        'id_cotizacion':pk,
                        'id_producto':detalle.id_producto.descripcion,
                        'cantidad':detalle.cantidad,
                        'valor':detalle.valor,
                        'fecha_ingreso':str(detalle.fecha_ingreso )                  
                    })
                responseData = {
                    'status': 'success',
                    'code': 200,
                    'msj': 'Factura encontrada',
                    'cotizacion': {
                        'id':cotizacion.id,
                        'cliente':cotizacion.cliente.nombre+' '+cotizacion.cliente.apellido,
                        'subtotal':cotizacion.subtotal,
                        'total':cotizacion.total,
                        'envio':cotizacion.envio,
                        'estado':cotizacion.estado,
                        'fecha_ingreso':fecha_ingreso                 
                    },
                  'detalle_cotizacion': detalle_cotizacion_json
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
        return render(request, 'cotizacion/modal-cotizacion.html', {'dato': responseData})
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