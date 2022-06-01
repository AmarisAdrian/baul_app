from django.contrib import admin
from app.config.models import LogModel,NotificacionModel

class LogAdmin(admin.ModelAdmin):
    list_display = ['id','modulo','excepcion', 'request']
    search_fields = ['id','modulo','excepcion', 'request']

class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['id','referencia','modulo','descripcion', 'estado','fecha_ingreso']
    search_fields = ['id','referencia','modulo','descripcion','estado', 'fecha_ingreso']

admin.site.register(LogModel,LogAdmin)
admin.site.register(NotificacionModel,NotificacionAdmin)
