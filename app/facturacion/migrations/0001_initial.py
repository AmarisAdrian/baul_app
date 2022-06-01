# Generated by Django 3.1.7 on 2022-01-27 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0001_initial'),
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacturacionModel',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('numero_factura', models.BigIntegerField(db_column='numero_factura')),
                ('subtotal', models.BigIntegerField(db_column='subtotal')),
                ('total', models.BigIntegerField(db_column='total')),
                ('envio', models.BigIntegerField(db_column='envio')),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True, db_column='fecha_ingreso')),
                ('adjunto', models.FileField(blank=True, db_column='adjunto', default=None, null=True, upload_to='pdf/')),
                ('cliente', models.ForeignKey(db_column='cliente', on_delete=django.db.models.deletion.CASCADE, to='cliente.clientemodel')),
            ],
            options={
                'verbose_name': 'Facturacion',
                'verbose_name_plural': 'facturaciones',
                'db_table': 'facturacion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DetalleFacturacionModel',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('cantidad', models.BigIntegerField(db_column='cantidad')),
                ('valor', models.BigIntegerField(db_column='valor')),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True, db_column='fecha_ingreso')),
                ('id_factura', models.ForeignKey(db_column='id_factura', on_delete=django.db.models.deletion.CASCADE, to='facturacion.facturacionmodel')),
                ('id_producto', models.ForeignKey(db_column='id_producto', on_delete=django.db.models.deletion.CASCADE, to='producto.productomodel')),
            ],
            options={
                'verbose_name': 'Detalle facturacion',
                'verbose_name_plural': 'Detalle facturacion',
                'db_table': 'detalle_facturacion',
                'managed': True,
            },
        ),
    ]
