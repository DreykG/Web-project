from django.shortcuts import render
import random
from decimal import Decimal

from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, action
# from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status,viewsets
from .models import Case, CaseItem, CaseOpening
from shop.models import InventoryItem
from shop.serializers import InventoryItemSerializer
from .serializers import CaseItemSerializer, CaseOpeningSerializer, CaseSerializer
from django.db import transaction


class CaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Case.objects.filter(is_active=True)
    serializer_class = CaseSerializer
    # permission_classes = []

    @action(detail=True, methods=['get'])
    def case_items(self, request, pk=None):
        case = self.get_object()
        items = case.case_items.all()
        serializer = CaseItemSerializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def open_case(self, request, pk=None):
        user = request.user
        case = self.get_object()

        # has_pending = InventoryItem.objects.filter(
        #     user=user, 
        #     status='pending'
        # ).exists()

        # if has_pending:
        #     return Response(
        #         {"detail": "You have an unresolved issue! Sell it first or accept it!"}, 
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        if user.balance < case.price:
            return Response({"detail" : "Not enought balance!"}, status=status.HTTP_400_BAD_REQUEST)
        
        items_queryset = case.case_items.all()
        case_items = list(items_queryset)

        weights = [float(item.drop_chance) for item in case_items]

        winning_case_item = random.choices(case_items, weights=weights, k=1)[0]

        with transaction.atomic():
            user.balance -= case.price
            user.save()
        
            new_item = InventoryItem.objects.create(
                user=user,
                skin=winning_case_item.skin,
                wear=winning_case_item.wear,
                price=winning_case_item.skin.base_price,
                status='pending',
                obtained_type='case'
            )

            CaseOpening.objects.create(
                user=user,
                case=case,
                case_item=winning_case_item,
                inventory_item=new_item,
                   spent_balance=case.price,
            )
        return Response({
            "item_id": new_item.id,
            "skin_name": winning_case_item.skin.name,
            "sell_price": new_item.price,
            "drop": InventoryItemSerializer(new_item).data
        })
    
    @action(detail=False, methods=['get'])
    def pending_items(self, request):
        user = request.user
        items = InventoryItem.objects.filter(user=user, status='pending').order_by('-created_at')
        serializer = InventoryItemSerializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def sell_dropped_item(self, request):
        item_id = request.data.get('item_id')
        user = request.user

        item = get_object_or_404(InventoryItem, id=item_id, user=user, status='pending')

        with transaction.atomic():
            user.balance += item.price
            user.save()

            item.delete()
        return Response({"detail": f"Sold for {item.price}"})
    
    @action(detail=False, methods=['post'])
    def access_dropped_item(self, request):
        item_id = request.data.get('item_id')
        user=request.user
        item = get_object_or_404(InventoryItem, id=item_id, user=user, status='pending')

        item.status = 'in_inventory'
        item.save()

        return Response({"detail" : "Item added to inventory!"})

