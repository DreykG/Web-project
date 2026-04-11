from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse
from django.urls import path, include

from ..views import ProfileViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    # path('admin/', admin.site.urls),
    
    path('', include(router.urls)),
]
