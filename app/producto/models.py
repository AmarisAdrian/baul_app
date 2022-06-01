from django.db import models

    
class ProductoModel(models.Model):
    MOTIVO_CHOICES= (
        (1,"Niño"),
        (2,"Niña"),
    )
    id = models.AutoField(db_column='id', primary_key=True)
    codigo = models.BigIntegerField( db_column='codigo')
    descripcion = models.CharField(db_column='descripcion', max_length=300)
    detalle_producto = models.CharField(db_column='detalle_producto', max_length=300)
    talla = models.CharField(db_column='talla', max_length=100)
    precio_unitario = models.BigIntegerField(db_column='precio_unitario', blank=True)
    valor = models.BigIntegerField(db_column='valor')
    valor_venta = models.BigIntegerField(db_column='valor_venta')
    descuento = models.FloatField(db_column='descuento')
    cantidad = models.IntegerField(db_column='cantidad', blank=True)   
    valor_descuento = models.BigIntegerField(db_column='valor_descuento')
    id_motivo = models.IntegerField(db_column='id_motivo', choices=MOTIVO_CHOICES)
    referencia = models.IntegerField( db_column='referencia', unique=True)
    fecha_ingreso = models.DateTimeField(db_column='fecha_ingreso', auto_now_add=True)
    pieza = models.IntegerField(db_column='pieza')

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = True
        db_table = 'producto'
        verbose_name="Productos"
        verbose_name_plural= 'productos' 

    
class ImagenProductoModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    producto = models.ForeignKey(ProductoModel, on_delete=models.CASCADE, db_column='id_producto')
    descripcion = models.CharField(db_column='descripcion', max_length=300)
    adjunto = models.FileField(upload_to='img/producto/', db_column='adjunto',blank=True, null=True,default=None)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = True
        db_table = 'imagen-producto'
        verbose_name="imagen-producto"
        verbose_name_plural= 'imagenes-productos' 