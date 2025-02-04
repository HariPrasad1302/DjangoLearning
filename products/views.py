from django.shortcuts import render
from .models import ProductDatas
from apis.models import UserData
from apis.serializers import UserDataSerializer
from .serializers import ProductSerializer

# Create your views here.

def multidb(request):
    products = ProductDatas.objects.all()
    product_serializer = ProductSerializer(products, many=True)
    users = UserData.objects.all()
    user_serializer = UserDataSerializer(users, many=True)

    print("Users:", user_serializer.data) 
    print("Products:", product_serializer.data)
    response = {
        "products": product_serializer.data,
        "users": user_serializer.data,
    }
    return render(request, 'data.html', response)