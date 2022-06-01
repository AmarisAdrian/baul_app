from django.urls import path,include
from app.cliente.views import ConsultarCliente, index , CreateCliente, UpdateCliente, DeleteCliente

app_name = 'app.cliente'
urlpatterns = [
    path('', index.as_view(), name="cliente"),
    path('lista-cliente', ConsultarCliente, name="lista-cliente"),
    path('crear-cliente', CreateCliente.as_view(), name="crear-cliente"),
    path('editar-cliente/<pk>/', UpdateCliente.as_view(), name="editar-cliente"),
    path('eliminar-cliente/<pk>/',DeleteCliente.as_view(), name="eliminar-cliente"),
]