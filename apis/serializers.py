from rest_framework import serializers
from .models import UserData, UserWishlist, ProductData

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductData
        fields = ['id', 'product_name', 'product_price', 'image']

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id','mobile_number', 'email', 'name']

class UserWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWishlist
        fields = ['id', 'product_name', 'product_description', 'product_price']


class UserWithWishlistSerializer(serializers.ModelSerializer):
    wishlist = serializers.SerializerMethodField()
    class Meta:
        model = UserData  
        fields = ['id', 'name', 'email', 'mobile_number', 'wishlist']

    def get_wishlist(self, obj):
        wishlist_items = UserWishlist.objects.filter(user=obj) 
        return [
            {
                "id": item.id,
                "product_name": item.product_name,
                "product_description": item.product_description,
                "product_price": item.product_price
            } for item in wishlist_items
        ]
        
class GenerateTokenSerializer(serializers.Serializer):
        email = serializers.EmailField()