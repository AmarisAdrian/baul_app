from django.contrib import admin
from app.stock.models import StockModel

class StockAdmin(admin.ModelAdmin):
    list_display = ['id','fecha_movimiento','precio_unitario', 'valor', 'valor_venta', 'descuento', 'cantidad', 'valor_descuento',
    'motivo_traslado', 'id_producto']
    search_fields = ['id','id_producto','fecha_movimiento']

admin.site.register(StockModel,StockAdmin)


