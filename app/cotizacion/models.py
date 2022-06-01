from app.cliente.models import ClienteModel
from app.producto.models import ProductoModel
from django.db import models

# Create your models here.
class CotizacionModel(models.Model):
    ESTADO_CHOICES= (
        (1,'Cotizada'),
        (2,'Facturada')
    )
    id = models.AutoField(db_column='id',primary_key=True)
    cliente = models.ForeignKey(ClienteModel, on_delete=models.CASCADE, db_column='cliente')
    subtotal = models.BigIntegerField(db_column='subtotal')
    total = models.BigIntegerField(db_column='total')
    envio = models.BigIntegerField(db_column='envio')
    estado = models.IntegerField(db_column='estado', choices=ESTADO_CHOICES,default=1)
    fecha_ingreso = models.DateTimeField(db_column='fecha_ingreso', auto_now_add=True)
    adjunto = models.FileField(upload_to='pdf/',db_column='adjunto',blank=True, null=True)

    def __str__(self):
        return self.estado

    class Meta:
        managed = True
        db_table = 'cotizacion'
        verbose_name="Cotizacion"
        verbose_name_plural= 'cotizaciones' 


class DetalleCotizacionModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    id_cotizacion = models.ForeignKey(CotizacionModel, on_delete=models.CASCADE, db_column='id_cotizacion')
    id_producto = models.ForeignKey(ProductoModel, on_delete=models.CASCADE, db_column='id_producto')
    cantidad = models.BigIntegerField(db_column='cantidad')
    valor = models.BigIntegerField(db_column='valor')
    fecha_ingreso = models.DateTimeField(db_column='fecha_ingreso', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'detalle_cotizacion'
        verbose_name="Detalle cotizacion"
        verbose_name_plural= 'Detalle cotizacion' 