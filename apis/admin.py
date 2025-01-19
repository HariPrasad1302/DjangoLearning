from django.contrib import admin
from .models import UserData

@admin.register(UserData)
class User(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_number') 
    search_fields = ('name', 'email', 'mobile_number') 