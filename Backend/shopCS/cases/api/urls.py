from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse
from django.urls import path, include

from ..views import CaseViewSet

router = DefaultRouter()
router.register(r'list', CaseViewSet, basename='case')

urlpatterns = [
    # path('admin/', admin.site.urls),
    
    path('', include(router.urls)),
]
