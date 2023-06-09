# Generated by Django 3.1.7 on 2022-01-27 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockModel',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('fecha_movimiento', models.DateTimeField(auto_now_add=True, db_column='fecha_movimiento')),
                ('precio_unitario', models.BigIntegerField(blank=True, db_column='precio_unitario')),
                ('valor', models.BigIntegerField(db_column='valor')),
                ('valor_venta', models.BigIntegerField(db_column='valor_venta')),
                ('descuento', models.FloatField(db_column='descuento')),
                ('cantidad', models.IntegerField(blank=True, db_column='cantidad')),
                ('valor_descuento', models.BigIntegerField(db_column='valor_descuento')),
                ('motivo_traslado', models.CharField(db_column='motivo_traslado', max_length=300)),
                ('id_producto', models.ForeignKey(db_column='id_producto', on_delete=django.db.models.deletion.CASCADE, to='producto.productomodel')),
            ],
            options={
                'verbose_name': 'stock',
                'verbose_name_plural': 'stock',
                'db_table': 'stock',
                'ordering': ['-fecha_movimiento'],
                'get_latest_by': ['fecha_movimiento'],
                'managed': True,
            },
        ),
    ]
