from django.contrib import admin
from app.producto.models import ProductoModel , ImagenProductoModel
from app.producto.resources import ProductoResource
from import_export.admin import ImportExportModelAdmin

class ProductoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','codigo','descripcion', 'detalle_producto', 'talla', 'precio_unitario','valor',  'valor_venta', 
        'descuento', 'cantidad','valor_descuento', 'id_motivo', 'referencia', 'pieza']
    search_fields = ['id','codigo','descripcion','talla','referencia','id_motivo']
    resource_class = ProductoResource

class ImagenProductoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','producto','descripcion','adjunto']
    search_fields = ['id','producto']

admin.site.register(ProductoModel,ProductoAdmin)
admin.site.register(ImagenProductoModel,ImagenProductoAdmin)
