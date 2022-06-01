from django.urls import path,include
from app.stock.views import Stock,MovimientoStock,UpdateStock,ComparacionStock, Inventario,CruzarInventario, Inventariar,RelacionarInventario
app_name = 'app.stock'
urlpatterns = [
    #path('stock', Stock, name="stock"),
    path('stock', Stock.as_view(), name="stock"),
    path('inventario', Inventario.as_view(), name="inventario"),
    path('modal-comparacion', ComparacionStock.as_view(), name="modal-comparacion"),
    path('movimiento-stock/<pk>', UpdateStock.as_view(), name="movimiento-stock"),
    path('cruzar-inventario', CruzarInventario, name="cruzar-inventario"),
    path('inventariar', Inventariar.as_view(), name="inventariar"),
    path('relacionar-inventario',RelacionarInventario, name="relacionar-inventario"),
]
