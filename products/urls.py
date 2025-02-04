from django.urls import path
from .views import multidb
urlpatterns = [
    path('sample/', multidb, name='multi_db'),
]