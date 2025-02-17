from django.contrib import admin
from .models import ProductDatas
# Register your models here.

@admin.register(ProductDatas)

class ProductDatas(admin.ModelAdmin):
    list_display = ('id','product_name', 'product_description') 
    search_fields = ('product_name', 'product_description') 
  