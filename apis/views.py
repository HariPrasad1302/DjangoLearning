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
    def get( request):
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
    def get(request,userID):
        
        user = UserData.objects.get(id= userID)
        wishlistData = user.wishlist.all()
        wishlistSerializer = UserWishlistSerializer(wishlistData, many = True)

        return Response({
                "status": 200,
                "message": "User wishlist fetched successfully",
                "user": UserDataSerializer(user).data,
                "wishlist": wishlistSerializer.data
            })


