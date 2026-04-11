from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from ..views import ProfileViewSet, register

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    # path('admin/', admin.site.urls),
    
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='login'),
    path('register/', register, name='register')
]
