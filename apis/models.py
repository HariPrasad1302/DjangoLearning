from django.db import models

# Create your models here.
class UserData(models.Model):
    
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)