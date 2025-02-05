from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserData, UserWishlist
from .serializers import UserDataSerializer, UserWishlistSerializer, GenerateTokenSerializer
from rest_framework_simplejwt.tokens import AccessToken
from drf_spectacular.utils import extend_schema
from django.utils.translation import gettext as _
from datetime import datetime
import locale
from django.utils.formats import localize
from django.utils import timezone
from django.conf import settings
import pytz
import logging
from .forms import user_reg, modelUser_reg

# Create your views here.

class userDetail(APIView):
    def get(self, request):
        user_data = [
            {
                "id": 1,
                "mobile_number": "1234556789",
                "email": "abc@gamil.com",
                "name": "John"
            },
            {
                "id": 2,
                "mobile_number": "1234556788",
                "email": "mic@gamil.com",
                "name": "Micheal"
            }
        ]

        return render(request, 'index.html', {"user_data": user_data})
        

#Using serializer
class UserDetailAPI(APIView):
    def get(self, request):
        users = UserData.objects.all()
        serializer = UserDataSerializer(users, many=True)
        return Response({
            "status":200,
            "message": "success",
            "data": serializer.data
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

            if not UserData.objects.filter(email=email).exists():
                return Response({"status": 404, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            token = AccessToken()
            token['email'] = email

            return Response({
                "status": 200,
                "message": "Token generated successfully",
                "token": str(token)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserWishlistApi(APIView):
    def get(self, request):     
        users = UserData.objects.all()
        responseData = []
        for user in users: 
            wishlistData = user.wishlist.all()
            userDatas = UserDataSerializer(user).data
            wishlistSerializer = UserWishlistSerializer(wishlistData, many = True).data
            
            responseData.append({
                "user": userDatas,
                "wishlistData": wishlistSerializer
            })
            
        
        return Response({
                "status": 200,
                "message": "Fetched all users with wishlist data successfully",
                "data": responseData
            })


#using prefetch_related method

class prefetch_wishlistData(APIView):
    def get(self, request):
        users = UserData.objects.prefetch_related('wishlist')
        response_data = []
        for user in users:
            userSerializer = UserDataSerializer(user).data
            wishlistSerializer = UserWishlistSerializer(user.wishlist.all(), many="True").data

            response_data.append({
                "user": userSerializer,
                "wishlist": wishlistSerializer
            })

        return Response({
            "status": 200,
            "message":"Wishlist Data fetched using prefetch_related",
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