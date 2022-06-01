from django.db import models

# Create your models here.

class ClienteModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    documento = models.BigIntegerField( db_column='documento',unique= True)
    nombre = models.CharField( db_column='nombre', max_length=300)
    apellido = models.CharField(db_column='apellido', max_length=300)
    direccion = models.CharField(db_column='direccion', max_length=300)
    telefono = models.BigIntegerField(db_column='telefono')
    email = models.EmailField(db_column='email',blank=True,null=True)
    fecha_ingreso = models.DateTimeField(db_column='fecha_ingreso', auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)

    class Meta:
        managed = True
        db_table = 'cliente'
        verbose_name="cliente"
        verbose_name_plural= 'clientes'
