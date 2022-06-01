from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from app.producto.models import ProductoModel
from django.contrib import admin
from django import forms  



class ProductoResource(resources.ModelResource):
  class Meta:  
    model = ProductoModel  

