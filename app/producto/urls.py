from django.urls import path,include
from app.producto.views import *
app_name = 'app.producto'
urlpatterns = [
    path('',index.as_view(),name="producto"),
    path('catalogo',indexCatalogo.as_view(),name="catalogo"),
    path('crear-producto', CreateProducto.as_view(), name="crear-producto"),
    path('editar-producto/<pk>/', UpdateProducto.as_view(), name="editar-producto"),
    path('eliminar-producto/<pk>/',DeleteProducto.as_view(), name="eliminar-producto"),
    path('importar-producto/',ImportarProducto, name="importar-producto"),
    path('consultar-producto/',ConsultarProducto, name="consultar-producto"),
    path('notificacion/',NotificacionStockProducto, name="notificacion"),
    path('consultar-producto-inventario/',ConsultarProductoInventario, name="consultar-producto-inventario"),
    path('consultar-producto-modal/<pk>/',ConsultarProductoModal,name="consultar-producto-modal"),
    path('crear-imagen-producto',CreateImagenProducto,name="crear-imagen-producto")
]