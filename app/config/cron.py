from app.producto.views import NotificacionStockProducto
from app.config.views import RegistrarLog
import logging

def notificaciones(self):
    logger = logging.getLogger()
    RegistrarLog('CRON', 'Cron ejecutado','NULL') 
    NotificacionStockProducto()
