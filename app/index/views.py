from django.shortcuts import render
from app.producto.models import ProductoModel
from app.facturacion.models import FacturacionModel
from app.cliente.models import ClienteModel
from app.config.models import NotificacionModel
from django.db.models import Sum
from django.http import JsonResponse
import logging
from app.config.views import RegistrarLog
from django.contrib.auth.decorators import login_required
from django.db import models,connection
import json

@login_required
def index(request):
    model = ProductoModel
    cliente_model = ClienteModel
    facturacion_model = FacturacionModel
    notificacion_model = NotificacionModel
    logger = logging.getLogger()
    modulo = "index/index"
    try:
        producto_count = model.objects.count()
        notificacion_count = NotificacionModel.objects.filter(estado=False).count() 
        notificacion_msj =  NotificacionModel.objects.filter(estado=False)
        Factura_count  = facturacion_model.objects.count()
        Factura_total = facturacion_model.objects.aggregate(sum = Sum('total'))['sum']
        Ranking = GetRankingCliente();
    except Exception as ex:
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
    return render(request,'layout/index.html',locals())

@login_required
def venta_anual(request):
    logger = logging.getLogger()
    venta_anual = GetTotalVentaAnual()
    try:
        if venta_anual:
            responseData = {
                'status': 'success',
                'code': 200,
                'msj': 'Grafica generada',
                'datos': {
                    'venta':venta_anual                        
                }
            }
        else:
            responseData = {
                'status': 'error',
                'code': 500,
                'msj': 'Grafica no generada'
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
def venta_producto(request):
    logger = logging.getLogger()
    facturacion_model = FacturacionModel
    venta = GetRankingProducto()
    try:
        if venta:
            responseData = {
                'status': 'success',
                'code': 200,
                'msj': 'Grafica generada',
                'datos': {
                    'venta':venta                        
                }
            }
        else:
            responseData = {
                'status': 'error',
                'code': 500,
                'msj': 'Grafica no generada'
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
def DetalleNotificacion(request, pk):
    model = NotificacionModel
    modulo = "index/DETALLENOTIFICACION"
    logger = logging.getLogger()
    try:
        if  pk != '' or pk != None :
            notificacion = NotificacionModel.objects.filter(id = pk).exists()
            if notificacion:
                notificacion = NotificacionModel.objects.get(id=pk)
                notificacion.estado = True
                notificacion.save()
                save = True
                if save:
                    responseData = {
                        'status': 'success',
                        'code': 200,
                        'msj': 'Notificacion encontrada',
                        'notificacion': {
                            'modulo':notificacion.modulo,
                            'descripcion':notificacion.descripcion,
                            'fecha':notificacion.fecha_ingreso 
                        }            
                    }
                else:
                    RegistrarLog(modulo,'Estado de notificacion no pudo actualizarse','NULL')

            else:
                responseData = {
                    'status': 'error',
                    'code': 500,
                    'msj': 'Notificacion no encontrada'
                }
        else:
             responseData = {
                'status': 'error',
                'code': 500,
                'msj': 'Error de validacion'
                }
        return render(request, 'layout/modal-notificacion.html', {'dato': responseData})            
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: ' + str(ex)
        }
        RegistrarLog(modulo,str(ex),'NULL')
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
    return JsonResponse(responseData,safe=False)

            

def GetRankingCliente():
    try:
        modulo = "index/GetRankingCliente"
        logger = logging.getLogger()
        with connection.cursor() as cursor:         
                cursor.execute("select c.id, c.nombre , c.apellido ,sum(f.total) as total ,count(*) as cantidad " +
                                           "from facturacion f " +
                                           "inner join cliente c on f.cliente = c.id " +
                                           "group by c.id ,c.nombre , c.apellido")
                data = cursor.fetchall()
                return data
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: ' + str(ex)
        }
        RegistrarLog(modulo,str(ex),'NULL')
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
    return JsonResponse(responseData,safe=False)
        

def GetTotalVentaAnual():
    try:
        modulo = "index/GetTotalVentaAnual"
        logger = logging.getLogger()
        with connection.cursor() as cursor:         
                cursor.execute("SELECT " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 1,  total, 0)) AS Enero , " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 2,  total, 0)) AS Febrero, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 3,  total, 0)) AS Marzo, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 4,  total, 0)) AS Abril, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 5,  total, 0)) AS Mayo, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 6,  total, 0)) AS Junio, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 7,  total, 0)) AS Julio, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 8,  total, 0)) AS Agosto, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 9,  total, 0)) AS Septiembre, " + 
                    "SUM(IF(MONTH(f.fecha_ingreso) = 10, total, 0)) AS Octubre, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 11, total, 0)) AS Noviembre, " +
                    "SUM(IF(MONTH(f.fecha_ingreso) = 12, total, 0)) AS Diciembre " +
                    "FROM facturacion f " +
                    "WHERE f.fecha_ingreso BETWEEN  DATE_FORMAT(now(),'%Y-01-01') and DATE_FORMAT(now(),'%Y-12-31')")
                data = cursor.fetchall()
                return data
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: ' + str(ex)
        }
        RegistrarLog(modulo,str(ex),'NULL')
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
        return JsonResponse(responseData,safe=False)

def GetRankingProducto():
    try:       
        modulo = "index/GetRankingProducto"
        logger = logging.getLogger()
        with connection.cursor() as cursor:         
                cursor.execute("select  df.id_producto, p.descripcion ,COUNT(df.id_producto) as cantidad " + 
                    "from facturacion f " +
                    "inner join detalle_facturacion df on f.id = df.id_factura  " +
                    "inner join producto p on p.id = df.id_producto " +
                    "GROUP by  p.descripcion,df.id_producto " +
                    "order by cantidad desc  " +
                    "limit 5")
                data = cursor.fetchall()
                return data
    except Exception as ex:
        responseData = {
            'status': 'error',
            'code': 500,
            'msj': 'Informacion no procesada: ' + str(ex)
        }
        RegistrarLog(modulo,str(ex),'NULL')
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))
        return JsonResponse(responseData,safe=False)
