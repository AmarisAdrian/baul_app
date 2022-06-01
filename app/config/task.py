from celery import shared_task
from app.config.views import RegistrarLog
from app.producto.views import NotificacionStockProducto

@shared_task
def notificaciones():
    NotificacionStockProducto()