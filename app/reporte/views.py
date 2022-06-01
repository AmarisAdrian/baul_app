from django.db import router
from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.conf import settings
from reportlab.pdfgen import canvas
from django.views.generic import View
from django.http import HttpResponse,FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from app.config.views import RegistrarLog
from app.facturacion.models import FacturacionModel , DetalleFacturacionModel
from app.cotizacion.models import CotizacionModel,DetalleCotizacionModel
from app.cliente.models import ClienteModel
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import logging , os ,time 
from io import BytesIO
from reportlab.lib.units import inch, cm
import random
from wsgiref.util import FileWrapper

# Create your views here.
class ImprimirFactura(LoginRequiredMixin,View):

    def header(self,pdf,no_factura,fecha):
        archivo_imagen = settings.MEDIA_ROOT+'img/Logo.png'
        pdf.drawImage(archivo_imagen, 30, 730, 110, 90,preserveAspectRatio=True) 
        pdf.setFillColorRGB(1,0,0)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(210, 780, u"FACTURA DE VENTA")

        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(220, 765, u"elbauldepollito2021@gmail.com")
        pdf.drawString(240, 755, u"Tel : 3004001398")
        pdf.drawString(230, 745, u"Barranquilla - colombia")

        pdf.setFillColorRGB(1,0,0)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(445, 780, u"N° FACTURA")
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(450, 760,no_factura)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(450, 745,fecha)

    def cliente(self,pdf,identificacion,nombre,direccion,telefono):
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(210, 670, u"DATOS CLIENTE")
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, 630, u"Identificacion : ")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(130, 630, identificacion)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, 610, u"Nombre : " )
        pdf.setFont("Helvetica", 12)
        pdf.drawString(130, 610, nombre)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(370, 630, u"Direccion : " )
        pdf.setFont("Helvetica", 12)
        pdf.drawString(440, 630,direccion)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(370, 610, u"Telefono : " )
        pdf.setFont("Helvetica", 12)
        pdf.drawString(440, 610,telefono)

    def tabla(self,pdf,id_Factura):
        y = 480
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(230, 550, u"PRODUCTOS")
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Producto', 'Cantidad', 'Valor')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(detalle.id_producto, detalle.cantidad, str('$ ')+' '+str(detalle.valor)) for detalle in DetalleFacturacionModel.objects.filter(id_factura =id_Factura )]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[10 * cm, 2 * cm, 5 * cm, 5 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 50,y)
    
    def total(self,pdf,total,envio):
        pdf.setFillColorRGB(1,0,0)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(350, 340, u"Envio:")
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(470, 340, envio)
        
        pdf.setFillColorRGB(1,0,0)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(350, 300, u"Total producto:")
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(470, 300, total)

    def get(self, *args, **kwargs):
        modulo = "ImprimirFactura/get"
        logger = logging.getLogger()
        id = kwargs['pk']
        requested = []
        try:
            if id != '' or id != None:
                factura = FacturacionModel.objects.filter(id = id).exists()
                if factura:
                    factura = FacturacionModel.objects.get(id = id)
                    cliente = ClienteModel.objects.get(id = factura.cliente.id)
                    fecha= factura.fecha_ingreso.strftime('%d-%m-%Y')
                    filename = str(cliente.documento)+str(fecha)+str(random.randint(0, 99))+str(".pdf")
                    response = HttpResponse(content_type='application/pdf')  
                    pdf = canvas.Canvas(settings.PDF_ROOT+filename)
                    self.header(pdf,str(factura.numero_factura),str(fecha))
                    self.cliente(pdf,str(cliente.documento),str(cliente.nombre) + ' ' + str(cliente.apellido),str(cliente.direccion),str(cliente.telefono))
                    self.tabla(pdf,factura.id)
                    self.total(pdf,str('$ ')+' '+str(factura.total),str('$ ')+' '+str(factura.envio))
                    pdf.showPage()
                    pdf.save()
                    route = settings.PDF_ROOT+filename 
                    if factura.adjunto == "" or factura.adjunto == "None" or factura.adjunto == None:
                       factura.adjunto = route
                       factura.save()
                    else:
                        cotizacion = FacturacionModel.objects.get(id = id)
                        cotizacion.adjunto = route
                        cotizacion.save()   
                    filename = route
                    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)            
                    return FileResponse(open(filename, 'rb'), content_type='application/pdf')
                else:
                    response = HttpResponse(content_type='application/pdf')
                    return response
        except Exception as ex:
            RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex),requested)
            logger.exception('Excepcion controlada: ' + str(ex))
            logger.error('Excepcion controlada: ' + str(ex))

        
class ImprimirCotizacion(LoginRequiredMixin,View):

    def header(self,pdf,no_cotizacion,fecha):
        archivo_imagen = settings.MEDIA_ROOT+'img/Logo.png'
        pdf.drawImage(archivo_imagen, 30, 730, 110, 90,preserveAspectRatio=True) 
        pdf.setFillColorRGB(1,0,0)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(240, 780, u"COTIZACION")

        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(220, 765, u"elbauldepollito2021@gmail.com")
        pdf.drawString(240, 755, u"Tel : 3004001398")
        pdf.drawString(230, 745, u"Barranquilla - colombia")

        pdf.setFillColorRGB(1,0,0)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(445, 780, u"N° COTIZACION")
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(450, 760,no_cotizacion)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(450, 745,fecha)

    def cliente(self,pdf,identificacion,nombre,direccion,telefono):
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(210, 670, u"DATOS CLIENTE")
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, 630, u"Identificacion : ")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(130, 630, identificacion)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, 610, u"Nombre : " )
        pdf.setFont("Helvetica", 12)
        pdf.drawString(130, 610, nombre)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(370, 630, u"Direccion : " )
        pdf.setFont("Helvetica", 12)
        pdf.drawString(440, 630,direccion)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(370, 610, u"Telefono : " )
        pdf.setFont("Helvetica", 12)
        pdf.drawString(440, 610,telefono)

    def tabla(self,pdf,id_cotizacion):
        y = 480
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(230, 550, u"PRODUCTOS")
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Producto', 'Cantidad', 'Valor')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(detalle.id_producto, detalle.cantidad, str('$ ')+' '+str(detalle.valor)) for detalle in DetalleCotizacionModel.objects.filter(id_cotizacion =id_cotizacion )]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[10 * cm, 2 * cm, 5 * cm, 5 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 50,y)
    
    def total(self,pdf,total,envio):
        pdf.setFillColorRGB(1,0,0)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(350, 340, u"Envio:")
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(470, 340, envio)
        
        pdf.setFillColorRGB(1,0,0)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(350, 300, u"Total producto:")
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(470, 300, total)

    def get(self, *args, **kwargs):
        modulo = "ImprimirCotizacion/get"
        logger = logging.getLogger()
        id = kwargs['pk']
        requested = []
        pdf = ""
        try:
            if id != '' or id != None:
                cotizacion = CotizacionModel.objects.filter(id = id).exists()
                if cotizacion:
                    cotizacion = CotizacionModel.objects.get(id = id)
                    cliente = ClienteModel.objects.get(id = cotizacion.cliente.id)
                    fecha= cotizacion.fecha_ingreso.strftime('%d-%m-%Y')
                    filename = str(cliente.documento)+str(fecha)+str(random.randint(0, 99))+str(".pdf")
                    response = HttpResponse(content_type='application/pdf')  
                    pdf = canvas.Canvas(settings.PDF_ROOT+filename)     
                    self.header(pdf,str(cotizacion.id),str(fecha))
                    self.cliente(pdf,str(cliente.documento),str(cliente.nombre) + ' ' + str(cliente.apellido),str(cliente.direccion),str(cliente.telefono))
                    self.tabla(pdf,cotizacion.id)
                    self.total(pdf,str('$ ')+' '+str(cotizacion.total),str('$ ')+' '+str(cotizacion.envio)) 
                    pdf.showPage() 
                    pdf.save()     
                    route = settings.PDF_ROOT+filename 
                    if cotizacion.adjunto == "" or cotizacion.adjunto == "None" or cotizacion.adjunto == None:
                       cotizacion.adjunto = route
                       cotizacion.save()
                    else:
                        cotizacion = CotizacionModel.objects.get(id = id)
                        cotizacion.adjunto = route
                        cotizacion.save()   
                    filename = route
                    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)            
                    return FileResponse(open(filename, 'rb'), content_type='application/pdf')
                else:
                    response = HttpResponse(content_type='application/pdf')
                    return response
        except Exception as ex:
            RegistrarLog(modulo, 'Excepcion controlada: '+ str(ex),requested)
            logger.exception('Excepcion controlada: ' + str(ex))
            logger.error('Excepcion controlada: ' + str(ex))

  
