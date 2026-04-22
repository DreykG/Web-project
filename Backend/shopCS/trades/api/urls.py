from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse
from django.urls import path, include
from ..views import TradeViewSet

router = DefaultRouter()
router.register(r'', TradeViewSet, basename='trades')

urlpatterns = [
    path('', include(router.urls)),
]
