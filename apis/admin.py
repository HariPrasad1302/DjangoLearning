from django.contrib import admin
from .models import UserData, UserWishlist

@admin.register(UserData)
class User(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'mobile_number') 
    search_fields = ('name', 'email', 'mobile_number') 

@admin.register(UserWishlist)
class Wishlists(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_name', 'product_description', 'product_price')
    search_fields = ('product_name', 'product_description')
  