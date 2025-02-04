from django.shortcuts import render
from .models import ProductDatas
from apis.models import UserData
from apis.serializers import UserDataSerializer

# Create your views here.

def multidb(request):
    products = list(ProductDatas.objects.all() )
    users = UserData.objects.all()
    user_serializer = UserDataSerializer(users, many=True)

    print("Users:", user_serializer.data)  # Debugging
    print("Products:", products)
    response = {
        "products": products,
        "users": user_serializer.data,
    }
    return render(request, 'data.html', response)