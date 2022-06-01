from django.urls import path
from app.cotizacion.views import index,CrearCotizacion,ConsultarCotizacion

app_name='app.cotizacion'
urlpatterns = [
    path('',index.as_view(),name='cotizacion'),
    path('crear-cotizacion',CrearCotizacion,name='crear-cotizacion'),
    path('consultar-cotizacion/<pk>',ConsultarCotizacion,name='consultar-cotizacion')
]
