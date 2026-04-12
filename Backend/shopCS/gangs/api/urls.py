from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse
from django.urls import path, include
from ..views import (
    GangViewSet
)

router = DefaultRouter()
router.register(r'', GangViewSet, basename='gangs')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include(router.urls)),
]
