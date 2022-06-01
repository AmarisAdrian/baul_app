from django.shortcuts import render
from app.facturacion.models import FacturacionModel
from app.config.models import LogModel
from datetime import date, datetime ,timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import logging
# Create your views here.
@csrf_exempt
def ConsultarConsecutivoFactura():
    model = FacturacionModel
    consecutivo_factura = 0
    now = date.today()
    format_fecha = now.strftime('%Y%m%d')
    consecutivo = "0"
    consecutivo = consecutivo.zfill(3) 
    no_factura = model.objects.order_by("-id").exists()
    if no_factura: 
        no_factura = model.objects.latest('fecha_ingreso')
        fecha_reg = no_factura.fecha_ingreso
        fecha_reg =  fecha_reg.strftime('%Y%m%d')
        if fecha_reg == format_fecha:
            consecutivo = int(no_factura.numero_factura)+ 1;
            consecutivo_factura = str(consecutivo);
        else :
            consecutivo_factura = format_fecha + str(consecutivo);
    else:
        consecutivo_factura = format_fecha + str(consecutivo);
    return consecutivo_factura


def RegistrarLog(modulo , Excepcion,*requested):
    model = LogModel
    logger = logging.getLogger()
    try:
        if modulo != '' and Excepcion != '' and requested != '':
            log = LogModel()
            log.modulo = modulo
            log.excepcion = Excepcion
            log.request = requested
            log.save()
        else: 
            logger.exception('Excepcion controlada: ' + str(ex))
            logger.error('Excepcion controlada: ' + str(ex))
    except Exception as ex:
        logger.exception('Excepcion controlada: ' + str(ex))
        logger.error('Excepcion controlada: ' + str(ex))


