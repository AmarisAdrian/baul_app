from django.urls import path, include
from .views import ListUsuario,UpdateUsuario

app_name = 'app.usuario'
urlpatterns = [  
    path('',ListUsuario.as_view(), name="usuario"),
    path('mi-perfil/<pk>/',UpdateUsuario.as_view(), name="mi-perfil"),
]