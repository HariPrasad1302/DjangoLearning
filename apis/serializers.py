from rest_framework import serializers
from .models import UserData, UserWishlist

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id','mobile_number', 'email', 'name']

class UserWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWishlist
        fields = ['id', 'productName', 'productDescription', 'productPrice']


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
                "productName": item.productName,
                "productDescription": item.productDescription,
                "productPrice": item.productPrice
            } for item in wishlist_items
        ]
        
class GenerateTokenSerializer(serializers.Serializer):
        email = serializers.EmailField()