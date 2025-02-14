from django.urls import path
from .views import multidb
urlpatterns = [
    path('sample/', multidb.as_view(), name='multi_db'),
]