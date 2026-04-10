from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse
from django.urls import path, include
from ..views import (
    CategoryListAPIView, 
    CategoryDetailAPIView, 
    WeaponListAPIView, 
    WeaponDetailAPIView, 
    InventoryItemViewSet,
    add_to_cart,
    checkout_selected,
    remove_from_cart,
    view_cart,
    for_sale,
    cancel_sale,
)

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet, basename='all-items')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('categories/', include('api.urls')),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:category_pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<int:category_pk>/weapons/', WeaponListAPIView.as_view(), name='weapon-list'),
    path('categories/<int:category_pk>/weapons/<int:weapon_pk>/', WeaponDetailAPIView.as_view(), name='weapon-detail'),
    path('categories/<int:category_pk>/weapons/<int:weapon_pk>/items/', 
        InventoryItemViewSet.as_view({'get': 'list'}),
        name='weapon_items'),


    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:item_id>', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/checkout', checkout_selected, name='checkout'),

    path('items/sale', for_sale, name='for_sale'),
    path('items/cancel_sale', cancel_sale, name='cancel_sale'),
    
    

    path('', include(router.urls)),
]
