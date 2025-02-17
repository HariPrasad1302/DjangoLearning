from rest_framework import serializers
from .models import ProductDatas

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDatas
        fields =['id', 'product_name', 'product_description']