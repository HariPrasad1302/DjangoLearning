from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserData, UserWishlist
from .serializers import UserDataSerializer, UserWithWishlistSerializer, GenerateTokenSerializer, UserWishlistSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.utils.translation import gettext as _
from datetime import datetime
import locale
from django.utils.formats import localize
from django.utils import timezone
from django.conf import settings

import pytz
import logging
import concurrent.futures
from .forms import user_reg, modelUser_reg
from asgiref.sync import sync_to_async
import time, asyncio


# Create your views here.
class userDetail(APIView):
    def get(self, request):
        users = UserData.objects.all()
        serializer = UserDataSerializer(users, many=True)

        return Response({
            "status":200,
            "message": "success",
            "count": len(serializer.data),
            "user_Data": serializer.data,
        })
        

#Using serializer
class UserDetailAPI(APIView):

    def get(self, request):
        users = UserData.objects.all()
        serializer = UserDataSerializer(users, many=True)
        user_names = map(lambda user: user.name, users) #lambda functions
        return Response({
            "status":200,
            "message": "success",
            "data": serializer.data,
            "user_name": user_names
        })
        
#token
class generateUserToken(APIView):
    @extend_schema(
        request=GenerateTokenSerializer,  
        responses={200: "Token generated successfully", 404: "User not found"}, 
    )
    def post(self, request):
        serializer = GenerateTokenSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            try:
                user = UserData.objects.get(email=email)  
            except UserData.DoesNotExist:
                return Response(
                    {"status": 404, "message": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            refresh = RefreshToken()
            refresh["email"] = user.email  
            refresh["user_name"] = user.name
            access = refresh.access_token

            return Response({
                "status": 200,
                "message": "Token generated successfully",
                "access_token": str(access),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserWishlistApi(APIView):
    def get(self, request):     
        users = UserData.objects.all()
        serializer = UserWithWishlistSerializer(users, many=True)  # Serialize all users
        return Response({
            "status": 200,
            "message": "Fetched all users with wishlist data successfully",
            "count": len(serializer.data),  # Count of users
            "data": serializer.data  # Serialized data
        })


#using prefetch_related method

class prefetch_wishlistData(APIView):
    def get(self, request):
        users = UserData.objects.prefetch_related('wishlist')  # Optimized query
        response_data = UserWithWishlistSerializer(users, many=True).data
        
        return Response({
            "status": 200,
            "message": "Wishlist Data fetched using prefetch_related",
            "data": response_data
        })


# using select_related method

class select_related_wishlistData(APIView):
    def get(self, request):
        wishlistData = UserWishlist.objects.select_related('user')
        response_data = []
        
        for data in wishlistData:
            userSerializer = UserDataSerializer(data.user).data
            wishlistSerializer = UserWishlistSerializer(data).data
            
            response_data.append({
                "user": userSerializer,
                "product": wishlistSerializer
            })
            
        return Response({
            "status": 200,
            "message": "Wishlist Data fetched using select_related",
            "data": response_data
        })
        

# Example for internalization and lcoalization

def translation(request):
    locale.setlocale(locale.LC_ALL, request.LANGUAGE_CODE)
    language_code = request.LANGUAGE_CODE
    timezone_str = settings.LANGUAGE_TIMEZONE_MAP.get(language_code, 'UTC')
    print(timezone_str)
    tz = pytz.timezone(timezone_str)
    print(tz)
    timezone.activate(tz)
    
    today = datetime.now(tz)
    Date = today.strftime('%B %d, %Y')
    amount = 3412.23
    response = {
        "message": _("Welcome to the Django Development"),
        "current_date": today,
        "price": locale.currency(amount, grouping=True)
    }
    return render(request, 'translation.html', response)


# Logging in Django

logger = logging.getLogger(__name__)

def logging_example(request):
    logger.info("This is an info log")
    try:
        UserData.objects.get(id=8)
    except UserData.DoesNotExist:
        logger.error("Employee with id %s does not exist", 8)
    return HttpResponse("Logging example")

# Forms and validation

def form_validation(request):
    if request.method == 'POST':
        user_fm = user_reg(request.POST)
        if user_fm.is_valid():
            nm = user_fm.cleaned_data['name']
            em = user_fm.cleaned_data['email']
            mb = user_fm.cleaned_data['mobile_number']
            
            print(f'Name: {nm}, Email: {em}, Mobile Number: {mb}')
    else:
        user_fm = user_reg()
    return render(request, 'forms.html', {'form': user_fm})


def modelForm_val(request):
    if request.method == 'POST':
        form = modelUser_reg(request.POST)
        if form.is_valid():
            nm = form.cleaned_data['name']
            em = form.cleaned_data['email']
            mb = form.cleaned_data['mobile_number']

            form.save()
            print("form saved successfully")
            
            print(f'Name: {nm}, Email: {em}, Mobile Number: {mb}')
    else:
        form = modelUser_reg()
    return render(request, 'forms.html', {'form': form})



#asynchronous function 
def sync_userData():
    print("retrieving user data")
    time.sleep(2)
    users = UserData.objects.all()
    print("user data:", users)
    print("user data retrieved")

def sync_wishlistData():
    print("retrieving wishlist data")
    time.sleep(5)
    wishlists = UserWishlist.objects.all()
    print("wishlist data:", wishlists)
    print("wishlist data retrieved")

async def async_userData():
    print("retrieving user data")
    await asyncio.sleep(2)
    users = sync_to_async(list)(UserData.objects.all())
    print("user data:", users)
    print("user data retrieved")

async def async_wishlistData():
    print("retrieving wishlist data")
    await asyncio.sleep(5)
    wishlists = sync_to_async(list)(UserWishlist.objects.all())
    print("wishlist data:", wishlists)
    print("wishlist data retrieved")

def sync_func(request):
    start_time = time.time()
    sync_userData()
    sync_wishlistData()
    total_time = time.time() - start_time
    print("total time", total_time)
    return HttpResponse("Both user data and wishlist data retrieved successfully")

async def async_func(request):
    start_time = time.time()
    task1 = asyncio.ensure_future(async_userData())
    task2 = asyncio.ensure_future(async_wishlistData())
    await asyncio.gather(task1, task2)
    total_time = time.time() - start_time
    print("total time", total_time)
    return HttpResponse("Both user data and wishlist data retrieved successfully")
    
