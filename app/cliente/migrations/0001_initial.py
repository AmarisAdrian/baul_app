# Generated by Django 3.1.7 on 2022-01-27 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteModel',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('documento', models.BigIntegerField(db_column='documento', unique=True)),
                ('nombre', models.CharField(db_column='nombre', max_length=300)),
                ('apellido', models.CharField(db_column='apellido', max_length=300)),
                ('direccion', models.CharField(db_column='direccion', max_length=300)),
                ('telefono', models.BigIntegerField(db_column='telefono')),
                ('email', models.EmailField(blank=True, db_column='email', max_length=254, null=True)),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True, db_column='fecha_ingreso')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'db_table': 'cliente',
                'managed': True,
            },
        ),
    ]