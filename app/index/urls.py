from django.urls import path,include
from . import views 
from django.conf import settings 
from django.conf.urls.static import static

app_name = 'app.index'
urlpatterns = [
    path('',views.index ,name="index"),    
    path('venta-anual',views.venta_anual ,name="venta-anual"), 
    path('venta-producto',views.venta_producto ,name="venta-producto"), 
    path('consultar-notificacion/<pk>', views.DetalleNotificacion, name="consultar-notificacion"),
]
