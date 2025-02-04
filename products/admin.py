from django.contrib import admin
from .models import ProductDatas
# Register your models here.

@admin.register(ProductDatas)

class ProductDatas(admin.ModelAdmin):
    list_display = ('id','productName', 'productDescription') 
    search_fields = ('productName', 'productDescription') 
  