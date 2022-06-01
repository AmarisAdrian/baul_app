from django.contrib import admin
from app.facturacion.models import FacturacionModel,DetalleFacturacionModel
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class FacturacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','numero_factura','cliente','subtotal','total','envio','adjunto']
    search_fields = ['id','numero_factura','cliente']

class DetalleFacturacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','id_factura','id_producto','cantidad','valor']
    search_fields = ['id','id_factura','id_producto']

admin.site.register(FacturacionModel,FacturacionAdmin)
admin.site.register(DetalleFacturacionModel,DetalleFacturacionAdmin)
