from django.urls import path

from .views import userDetail, UserDetailAPI, generateUserToken, UserWishlistApi

urlpatterns = [
    path('user-details/', userDetail.as_view(), name='user-details'),
    path('userData/', UserDetailAPI.as_view(), name='userData'),
    path('validateUser/', generateUserToken.as_view(), name='validateUser'),
    path('userWishlist/',  UserWishlistApi.as_view(), name='userWishlist'),
]