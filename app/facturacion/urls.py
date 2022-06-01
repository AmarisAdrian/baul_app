from django.urls import path,include
from app.facturacion.views import index, CreateFacturacion, GenerarFacturacion, ConsultarFactura,FacturarCotizacion
app_name = 'app.facturacion'
urlpatterns = [
    path('',index.as_view(),name="facturacion"),
    path('crear-facturacion', CreateFacturacion.as_view(), name="crear-facturacion"),
    path('generar-facturacion', GenerarFacturacion, name="generar-facturacion"),
    path('facturar-cotizacion', FacturarCotizacion, name="facturar-cotizacion"),
    path('consultar-factura/<pk>', ConsultarFactura, name="consultar-factura"),
]