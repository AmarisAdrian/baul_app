from django.contrib import admin
from app.cotizacion.models import CotizacionModel,DetalleCotizacionModel
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CotizacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','cliente','subtotal','total','envio','estado','adjunto']
    search_fields = ['id','cliente']

class DetalleCotizacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','id_producto','cantidad','valor']
    search_fields = ['id','id_producto']

admin.site.register(CotizacionModel,CotizacionAdmin)
admin.site.register(DetalleCotizacionModel,DetalleCotizacionAdmin)