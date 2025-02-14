from django.shortcuts import render
from .models import ProductDatas
from apis.models import UserData
from apis.serializers import UserDataSerializer
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class multidb(APIView):
    def get(self, request):
        products = ProductDatas.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        users = UserData.objects.all()
        user_serializer = UserDataSerializer(users, many=True)

        return Response({
            "status":200,
            "message": "success",
            "user_count": len(user_serializer.data),
            "product_count": len(product_serializer.data),
            "users": user_serializer.data,
            "products": product_serializer.data
        })
