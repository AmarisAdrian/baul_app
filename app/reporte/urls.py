from django.urls import path,include
from app.reporte.views import ImprimirCotizacion, ImprimirFactura


app_name = 'app.reporte'
urlpatterns = [
    path('imprimir-factura/<pk>/',ImprimirFactura.as_view(), name="imprimir-factura"),
    path('imprimir-cotizacion/<pk>/',ImprimirCotizacion.as_view(), name="imprimir-cotizacion"),
]