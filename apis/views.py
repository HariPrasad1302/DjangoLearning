from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserData, UserWishlist
from .serializers import UserDataSerializer, UserWithWishlistSerializer, GenerateTokenSerializer, UserWishlistSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from googletrans import Translator
from django.utils.translation import gettext as _
from datetime import datetime
import locale
from django.utils.formats import localize
from django.utils import timezone
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
import pytz
import logging
import concurrent.futures
from .forms import user_reg, modelUser_reg
from asgiref.sync import sync_to_async
import time, asyncio
from .pagination import CustomPagination

# Create your views here.
class userDetail(APIView):
    def get(self, request):
        users = UserData.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserDataSerializer(result_page, many=True)

        return paginator.get_paginated_response({
            "status":200,
            "message": "success",
            "count": len(users),
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
            "data": {
                "count": len(serializer.data),
                "result": serializer.data
            },
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
            "data": {
                "count": len(serializer.data),
                "result": serializer.data
            },
        })


#using prefetch_related method

class prefetch_wishlistData(APIView):
    def get(self, request):
        users = UserData.objects.prefetch_related('wishlist')  # Optimized query
        response_data = UserWithWishlistSerializer(users, many=True).data
        
        return Response({
            "status": 200,
            "message": "Wishlist Data fetched using prefetch_related",
            "data": {
                "count": len(response_data),
                "result": response_data
            },
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
            "count": len(userSerializer),
            "data": response_data
        })
        

# Example for internalization and lcoalization

def translation(request):

    translator = Translator()
    try:
        locale.setlocale(locale.LC_ALL, request.LANGUAGE_CODE)
    except Exception as e:
        print(f"Locale setting failed: {e}")

    language_code = request.LANGUAGE_CODE
    timezone_str = settings.LANGUAGE_TIMEZONE_MAP.get(language_code, 'UTC')
    print(timezone_str)

    try:
        tz = pytz.timezone(timezone_str)
        print(tz)
        timezone.activate(tz)
    except Exception as e:
        print(f"Timezone error: {e}")
        timezone.activate(pytz.utc)
    
    today = datetime.now(tz)
    Date = today.strftime('%B %d, %Y')
    amount = 3412.23
  
    input_text = ""
    translated_text = ""

    if request.method == 'POST':
        input_text = request.POST.get('input_text')

        if input_text:
            try:
                translated_text = translator.translate(input_text, src='en', dest=language_code).text
            except Exception as e:
                print(f"Translation error: {e}")

    response = {
        "message": _("Welcome to the Django Development"),
        "current_date": today,
        "Language_code": language_code,
        "price": locale.currency(amount, grouping=True),
        "input_text": input_text,
        "translated_text": translated_text
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
    


class UserDataViewSet(ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(result_page, many=True)
        u_count = queryset.count()

        return paginator.get_paginated_response({
            "status": 200,
            "message": "Fetched all user data successfully",
            "data":{
                "count": u_count,
                "result": serializer.data
            }
        })
    
class UserWithWishlistViewSet(ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserWithWishlistSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user_count = queryset.count()  

        return Response({
            "status": 200,
            "message": "Fetched all users with wishlist data successfully",
            "data": {
                "count": user_count,
                "result": serializer.data
            },
        })

#refelctions
def inspect_userdata(request):
    try:
        user = UserData.objects.get(id=1)  
        current_name = getattr(user, 'name', None)
        new_name = "Mark"
        setattr(user, 'name', new_name)
        user.save()

        has_email = hasattr(user, 'email')  

        user_type = type(user).__name__  

        user_attributes = dir(user) 

        response_text = f"Current name: {current_name}<br>"
        response_text += f"Updated name: {getattr(user, 'name', None)}<br>"
        response_text += f"Has 'emailID' attribute? {has_email}<br>"
        response_text += f"Type of the object: {user_type}<br>"
        response_text += f"List of attributes and methods: {user_attributes}"

        return HttpResponse(response_text)

    except UserData.DoesNotExist:
        return HttpResponse("UserData with ID 1 does not exist.")
