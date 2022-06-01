from django.contrib import admin
from django.urls import path, include  
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.index.urls', namespace='index')),
    path('cliente/', include('app.cliente.urls',namespace="cliente")),
    path('producto/', include('app.producto.urls',namespace="producto")),
    path('stock/', include('app.stock.urls',namespace="stock")),
    path('facturacion/', include('app.facturacion.urls',namespace="facturacion")),
    path('cotizacion/', include('app.cotizacion.urls',namespace="cotizacion")),
    path('configuracion/', include('app.config.urls',namespace="config")),
    path('usuario/', include('app.usuario.urls',namespace="usuario")),
    path('reporte/', include('app.reporte.urls',namespace="reporte")),
    path('perfil/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)