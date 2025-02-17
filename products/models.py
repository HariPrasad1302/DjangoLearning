from django.db import models

# Create your models here.
class ProductDatas(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'product_data'
        app_label = 'products'
        