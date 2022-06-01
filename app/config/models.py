from django.db import models
from app.stock.models import StockModel

class LogModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    modulo = models.CharField(db_column='modulo', max_length=300)
    request = models.CharField(db_column='request', max_length=800, null= True,blank=True)
    excepcion = models.CharField(db_column='excepcion', max_length=600)
    fecha_ingreso = models.DateTimeField(db_column='fecha_ingreso', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'log'
        verbose_name="log"
        verbose_name_plural= 'logs' 

class NotificacionModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    referencia =  models.ForeignKey(StockModel, on_delete=models.PROTECT, null=True,blank=True)  
    modulo = models.CharField(db_column='modulo', max_length=300)
    descripcion = models.CharField(db_column='descripcion', max_length=800, null= True,blank=True)
    estado = models.BooleanField(db_column='estado', max_length=600)
    fecha_ingreso = models.DateTimeField(db_column='fecha_ingreso', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'notificacion'
        verbose_name="notificacion"
        verbose_name_plural= 'notificaciones'