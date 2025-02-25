from django.db import models

# Create your models here.
class UserData(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

    # class Meta:
    #     ordering = ['email']


class UserWishlist(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE ,related_name="wishlist")
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
class ProductData(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    