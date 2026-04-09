from django.contrib import admin
from ..views import CategoryListAPIView, CategoryDetailAPIView, WeaponListAPIView, WeaponDetailAPIView
from django.http import HttpResponse
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('categories/', include('api.urls')),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:category_pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<int:category_pk>/weapons/', WeaponListAPIView.as_view(), name='weapon-list'),
    path('categories/<int:category_pk>/weapons/<int:weapon_pk>/', WeaponDetailAPIView.as_view(), name='weapon-detail'),
]
