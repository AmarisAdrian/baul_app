from django.db import models
from app.cliente.models import ClienteModel
from app.producto.models import ProductoModel
from django.db import models,connection
from django.conf import Settings, settings

# Create your models here.

class FacturacionModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    numero_factura = models.BigIntegerField( db_column='numero_factura')
    cliente = models.ForeignKey(ClienteModel, on_delete=models.CASCADE, db_column='cliente')
    subtotal = models.BigIntegerField(db_column='subtotal')
    total = models.BigIntegerField(db_column='total')
    envio = models.BigIntegerField(db_column='envio')
    fecha_ingreso = models.DateTimeField(db_column='fecha_ingreso', auto_now_add=True)
    adjunto = models.FileField(upload_to='pdf/', db_column='adjunto',blank=True, null=True,default=None)

    class Meta:
        managed = True
        db_table = 'facturacion'
        verbose_name="Facturacion"
        verbose_name_plural= 'facturaciones' 
    
    def GetRankingCliente():
        try:       
            with connection.cursor() as cursor:         
                cursor.execute("call  GetRankingCliente();")
                data = cursor.fetchall()
                return data
        except Exception as e:
            print(e)
        
    def GetTotalVentaAnual():
        try:       
            with connection.cursor() as cursor:         
                cursor.execute("call GetTotalVentaAnual();")
                data = cursor.fetchall()
                return data
        except Exception as e:
            print(e)
    
    def GetRankingProducto():
        try:       
            with connection.cursor() as cursor:         
                cursor.execute("call GetRankingProducto();")
                data = cursor.fetchall()
                return data
        except Exception as e:
            print(e)
    


class DetalleFacturacionModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    id_factura = models.ForeignKey(FacturacionModel, on_delete=models.CASCADE, db_column='id_factura')
    id_producto = models.ForeignKey(ProductoModel, on_delete=models.CASCADE, db_column='id_producto')
    cantidad = models.BigIntegerField(db_column='cantidad')
    valor = models.BigIntegerField(db_column='valor')
    fecha_ingreso = models.DateTimeField(db_column='fecha_ingreso', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'detalle_facturacion'
        verbose_name="Detalle facturacion"
        verbose_name_plural= 'Detalle facturacion' 
