from rest_framework import serializers
from .models import UserData, UserWishlist

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['mobile_number', 'email', 'name']

class UserWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWishlist
        fields = ['id', 'productName', 'productDescription', 'productPrice']