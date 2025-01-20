from django.db import models

# Create your models here.
class UserData(models.Model):
    
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

class UserWishlist(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE ,related_name="wishlist")
    productName = models.CharField(max_length=50)
    productDescription = models.CharField(max_length=200)
    productPrice = models.DecimalField(max_digits=10, decimal_places=2)