from django.contrib import admin
from app.cliente.models import ClienteModel

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id','documento','nombre','apellido','direccion','telefono','fecha_ingreso']
    search_fields = ['id','documento']

admin.site.register(ClienteModel,ClienteAdmin)