from django.contrib import admin
from .models import UserData, UserWishlist

@admin.register(UserData)
class User(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'mobile_number') 
    search_fields = ('name', 'email', 'mobile_number') 

@admin.register(UserWishlist)
class Wishlists(admin.ModelAdmin):
    list_display = ('id', 'user', 'productName', 'productDescription', 'productPrice')
    search_fields = ('productName', 'productDescription')
  