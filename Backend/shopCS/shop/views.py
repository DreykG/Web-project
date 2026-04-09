from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, action
# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status,viewsets
from .models import Category, Weapon, Skin, Cart, CartItem, InventoryItem
from .serializers import CategorySerializer, CartItemSerializer, WeaponSerializer

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Category(data=request)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPIView(APIView):
    def get_object(self, category_pk):
        return get_object_or_404(Category, pk=category_pk)

    def get(self,request,category_pk):
        category = self.get_object(category_pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, category_pk):
        category = self.get_object(category_pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_pk):
        category = self.get_object(category_pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class WeaponListAPIView(APIView):
    def get(self, request, category_pk): 
        weapons = Weapon.objects.filter(category_id=category_pk)
        serializer = WeaponSerializer(weapons, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Weapon(data=request)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeaponDetailAPIView(APIView):
    def get_object(self, weapon_pk):
        return get_object_or_404(Weapon, weapon_pk=weapon_pk)

    def get(self, request, category_pk, weapon_pk):
        weapon = get_object_or_404(Weapon, pk=weapon_pk, category_id=category_pk)
        serializer = WeaponSerializer(weapon)
        return Response(serializer.data)
    
    def put(self, request, weapon_pk):
        weapons = self.get_object(weapon_pk)
        serializer = WeaponSerializer(weapons, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, weapon_pk):
        weapons = self.get_object(weapon_pk)
        weapons.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)












@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def add_to_cart(request, inventory_item_id):
    try:
        inventory_item = InventoryItem.objects.get(id=inventory_item_id)
    except InventoryItem.DoesNotExist:
        return Response(
            {"error": "Item not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if inventory_item.user == request.user:
        return Response(
            {"error": "You cannot add your own item to cart."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if inventory_item.status != "in_inventory":
        return Response(
            {"error": "This item is not available."},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart, created = Cart.objects.get_or_create(user=request.user)

    if CartItem.objects.filter(cart=cart, inventory_item=inventory_item).exists():
        return Response(
            {"error": "Item already in cart."},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart_item = CartItem.objects.create(
        cart=cart,
        inventory_item=inventory_item
    )

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)