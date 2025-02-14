from django.urls import path, include
from .views import userDetail, UserDetailAPI, generateUserToken, UserWishlistApi, prefetch_wishlistData, select_related_wishlistData, translation, logging_example, form_validation, modelForm_val, sync_func, async_func, UserDataViewSet, UserWishlistViewSet, UserWithWishlistViewSet
from django.conf.urls.i18n import set_language
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserDataViewSet, basename='user')
router.register(r'wishlist', UserWishlistViewSet, basename='wishlist')
router.register(r'users-with-wishlist', UserWithWishlistViewSet, basename='users-with-wishlist')

urlpatterns = [
    path('user-details/', userDetail.as_view(), name='user-details'),
    path('userData/', UserDetailAPI.as_view(), name='userData'),
    path('validateUser/', generateUserToken.as_view(), name='validateUser'),
    path('userWishlist/',  UserWishlistApi.as_view(), name='userWishlist'),
    path('userWishlist/prefetch_related/', prefetch_wishlistData.as_view(), name='prefetchWishlist'),
    path('userWishlist/select_related/', select_related_wishlistData.as_view(), name='selectRelatedWishlist'),
    path('translationDemo/', translation, name='translation'),
    path('set_language/', set_language, name='set_language'),
    path('logs/', logging_example, name='logs'),
    path('form_user/', form_validation),
    path('modelForm_user/', modelForm_val),
    path('sync/', sync_func, name='sync_func'),
    path('async/', async_func, name='async_func'),
    path('', include(router.urls))
]

