from decimal import Decimal

from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, action
# from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status,viewsets
from .models import Category, Weapon, Skin, Cart, CartItem, InventoryItem
from .serializers import CategorySerializer, InventoryItemSelectionSerializer, WeaponSerializer, InventoryItemSerializer
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

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


class InventoryItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryItemSerializer

    def get_queryset(self):
        queryset = InventoryItem.objects.filter(status='on_sale')
        
        weapon_pk = self.kwargs.get('weapon_pk')
        if weapon_pk:
            queryset = queryset.filter(skin__weapon_id=weapon_pk)
            
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(skin__weapon__category_id=category_id)

        weapon_id = self.request.query_params.get('weapon')
        if weapon_id:
            queryset = queryset.filter(skin__weapon__weapon_id=weapon_id)

        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_items(self, request):
        user_items = InventoryItem.objects.filter(
            user=request.user, 
            status=InventoryItem.StatusChoices.IN_INVENTORY
        )
        
        serializer = InventoryItemSelectionSerializer(user_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_sales(self, request):
        user_items = InventoryItem.objects.filter(
            user=request.user, 
            status=InventoryItem.StatusChoices.ON_SALE
        )
        
        serializer = self.get_serializer(user_items, many=True)
        return Response(serializer.data)







@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = InventoryItem.objects.filter(cart_items__cart=cart)
    serializer = InventoryItemSerializer(items, many=True)
    total_price = sum(item.price for item in items)
    
    return Response({
        "cart_id": cart.id,
        "items": serializer.data,
        "total_items_count": items.count(),
        "total_price": total_price
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, item_id):

    item = get_object_or_404(InventoryItem, id=item_id, status='on_sale')

    if item.user == request.user:
        return Response(
            {"detail": "You can't add own item!"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    if CartItem.objects.filter(cart=cart, inventory_item=item).exists():
        return Response({"detail": "Item already in your cart"}, status=status.HTTP_400_BAD_REQUEST)
        
    CartItem.objects.create(cart=cart, inventory_item=item)
    item.status = InventoryItem.StatusChoices.IN_CART
    item.save()
    
    return Response({"detail": "Item was added to cart"}, status=status.HTTP_201_CREATED)


@api_view(['POST']) # Используем POST для передачи тела запроса
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    user = request.user
    # Ожидаем структуру: {"ids": [1, 3, 5]}
    item_ids = request.data.get('ids', [])

    if not item_ids:
        return Response(
            {"detail": "No IDs provided!"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    cart_items = CartItem.objects.filter(
        cart__user=user, 
        inventory_item_id__in=item_ids
    )

    if not cart_items.exists():
        return Response(
            {"detail": "No matching items found in your cart!"}, 
            status=status.HTTP_404_NOT_FOUND
        )

    InventoryItem.objects.filter(id__in=item_ids, cart_items__cart__user=user).update(status="on_sale")

    count = cart_items.count()
    cart_items.delete()
    
    return Response(
        {"detail": f"Successfully removed {count} items from cart!"}, 
        status=status.HTTP_200_OK
    )



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_selected(request):

    buyer = request.user
    selected_ids = request.data.get('ids', [])
    if not selected_ids:
        return Response({"detail": "Nothing not!"}, status=status.HTTP_400_BAD_REQUEST)
    
    items_to_buy = InventoryItem.objects.filter(
        id__in = selected_ids,
        cart_items__cart__user = buyer,
        status = 'in_cart'
    ).select_related('user')

    if not items_to_buy.exists():
        return Response({"detail": "Items not found in the cart!"}, status=status.HTTP_404_NOT_FOUND)
    
    total_price = sum(item.price for item in items_to_buy)

    if buyer.balance < total_price:
        return Response({"detail" : "Not enough balance!"}, status=status.HTTP_400_BAD_REQUEST)
    
    bought_items_ids = list(items_to_buy.values_list('id', flat=True))
    
    with transaction.atomic():
        buyer.balance -= total_price
        buyer.save()

        for item in items_to_buy:
            seller = item.user

            if seller:

                commission = item.price * Decimal('0.05')
                seller.balance += (item.price - commission)
                seller.save()

            item.user = buyer
            item.status = InventoryItem.StatusChoices.IN_INVENTORY
            item.save()

        CartItem.objects.filter(cart__user=buyer, inventory_item__in=bought_items_ids).delete()


    return Response({
        "detail": "Purchase",
        "spent": total_price,
        "new_balance": buyer.balance
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def for_sale(request):
    seller = request.user
    profile = seller.profile

    #{"items": [{"id": 1, "price": 1500.5}, ...]}
    items_data = request.data.get('items', [])
    
    if not items_data:
        return Response({"detail": "Nothing choosen!"}, status=status.HTTP_400_BAD_REQUEST)
    
    selected_ids = [item['id'] for item in items_data]
    
    prices_map = {item['id']: item['price'] for item in items_data}

    items_qs = InventoryItem.objects.filter(
        id__in=selected_ids,
        user=seller,
        status='in_inventory'
    )

    if not items_qs.exists():
        return Response({"detail": "No items found!"}, status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():
        for item in items_qs:
            new_price = prices_map.get(item.id)
            if new_price:
                profile.inventory_value -= item.price
                profile.save()

                item.price = new_price
                item.status = 'on_sale'
                item.save()


                

    return Response({"detail": f"Items for sale: {items_qs.count()}"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_sale(request):
    user = request.user
    #{"items": [{"id": 1}, ...]}
    selected_ids = request.data.get('ids', [])
    
    if not selected_ids:
        return Response({"detail": "No items to be withdrawn from sale"}, status=status.HTTP_400_BAD_REQUEST)

    items_to_cancel = InventoryItem.objects.filter(
        id__in=selected_ids,
        user=user,
        status='on_sale'
    )

    if not items_to_cancel.exists():
        return Response({"detail": "The products have not been found or are no longer on sale!"}, status=status.HTTP_404_NOT_FOUND)

    count = items_to_cancel.count()

    with transaction.atomic():
        for item in items_to_cancel:
            item.price = 0
            item.status = 'in_inventory'
            item.save()
            CartItem.objects.filter(inventory_item=item).delete()

    return Response({
        "detail": f"Successfully withdrawn from sale of items: {count}",
        "removed_ids": selected_ids
    }, status=status.HTTP_200_OK)