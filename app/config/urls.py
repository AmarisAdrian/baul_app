from django.urls import path,include
from app.config.views import ConsultarConsecutivoFactura
app_name = 'app.config'
urlpatterns = [
    path('consultar-consecutivo-factura/',ConsultarConsecutivoFactura, name="consultar-consecutivo-factura"),
]
