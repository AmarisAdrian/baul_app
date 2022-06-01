from django.db import models
from app.producto.models import ProductoModel


class StockModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    id_producto = models.ForeignKey(ProductoModel, on_delete=models.CASCADE, db_column='id_producto')
    cantidad = models.IntegerField(db_column='cantidad', blank=True)
    fecha_movimiento = models.DateTimeField(db_column='fecha_movimiento', auto_now_add=True)
    precio_unitario = models.BigIntegerField(db_column='precio_unitario', blank=True)
    valor = models.BigIntegerField(db_column='valor')
    valor_venta = models.BigIntegerField(db_column='valor_venta')
    descuento = models.FloatField(db_column='descuento')
    cantidad = models.IntegerField(db_column='cantidad', blank=True)   
    valor_descuento = models.BigIntegerField(db_column='valor_descuento')
    motivo_traslado = models.CharField(db_column='motivo_traslado', max_length=300)

    class Meta:
        managed = True
        db_table = 'stock'
        verbose_name="stock"
        verbose_name_plural= 'stock' 
        ordering = ['-fecha_movimiento']
        get_latest_by = ['fecha_movimiento']

    def __str__(self):
        return self.motivo_traslado

