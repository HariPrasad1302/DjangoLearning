from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserData, UserWishlist
from .serializers import UserDataSerializer, UserWishlistSerializer
from rest_framework_simplejwt.tokens import AccessToken

# Create your views here.

class userDetail(APIView):
    def get(self, request):
        user_data = [
            {
                "mobile_number": "1234556789",
                "email": "abc@gamil.com",
                "name": "Thamizh"
            },
            {
                "mobile_number": "1234556788",
                "email": "abcd@gamil.com",
                "name": "Arasi"
            }
        ]

        return Response({
            "status":200,
            "message": "success",
            "data": {
                "count": len(user_data),
                "result": user_data
            }
        })

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
    def post( request):
        email = request.data.get('email')
        print("Email:", email)
        
        if not UserData.objects.filter(email=email).exists():
            return Response({"status":404,"message": "User not found"})
        
        token = AccessToken() 
        token['email'] = email
        
        return Response({
            "status":200,
            "message": "Token generated successfully",
            "token": str(token)
        })
    

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
