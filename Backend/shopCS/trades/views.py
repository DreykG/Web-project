from django.shortcuts import render

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import TradeOffer, TradeOfferItem, TradeResponse, TradeResponseItem
from .serializers import TradeOfferSerializer, TradeResponseSerializer
from shop.models import InventoryItem

class TradeViewSet(viewsets.ModelViewSet):
    queryset = TradeOffer.objects.filter(status='open')
    serializer_class = TradeOfferSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        

        if self.action == 'list':

            return TradeOffer.objects.filter(status='open').exclude(creator=user)
        
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def my_offers(self, request):
        user = request.user
        offers = TradeOffer.objects.filter(creator=user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)
    

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        item_ids = request.data.get('items', [])

        items = InventoryItem.objects.filter(id__in=item_ids, user=user, status='in_inventory')

        if items.count() != len(item_ids):
            return Response({"detail": "Some items are unavailable"}, status=400)
        
        total_value = sum(item.skin.base_price for item in items)

        offer = TradeOffer.objects.create(
            creator=user,
            title=request.data.get('title', ''),
            offer_value=total_value,
            is_private=request.data.get('is_private', False),
            password=request.data.get('password', 'None')
        )

        for item in items:
            TradeOfferItem.objects.create(trade_offer=offer, inventory_item=item)
            item.status = 'on_trade'
            item.save()

        return Response(TradeOfferSerializer(offer).data, status=201)
    

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def respond(self, request, pk=None):
        offer = self.get_object()
        user = request.user

        item_ids = request.data.get('items', [])

        if user == offer.creator:
            return Response({"detail": "You can't respond to your trade!"}, status=400)

        if not (1 <= len(item_ids) <= 5):
            return Response({"detail": "1 to 5 items need to be added!"}, status=400)

        items = InventoryItem.objects.filter(id__in=item_ids, user=user, status='in_inventory')
        if items.count() != len(item_ids):
            return Response({"detail": "Items not allow or already in trade!"}, status=400)
        
        total_value = sum(item.skin.base_price for item in items)

        response = TradeResponse.objects.create(
            trade_offer=offer,
            responder=user,
            response_value=total_value
        )

        for item in items:
            TradeResponseItem.objects.create(trade_response=response, inventory_item=item)
            item.status = 'on_trade'
            item.save()

        return Response(TradeResponseSerializer(response).data)
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def verify_password(self, request, pk=None):
        offer = self.get_object()

        password = request.data.get('password', '')
        if password != offer.password:
            return Response({"detail": "Incorrect password"}, status=400)

        return Response({"detail": "Password verified successfully!"})


    @action(detail=True, methods=['post'], url_path='accept-response/(?P<response_id>[^/.]+)')
    @transaction.atomic
    def accept_trade(self, request, pk=None, response_id=None):
        offer = self.get_object()
        user = request.user
        
        if offer.creator != user:
            return Response({"detail": "Only creator can accept the trade"}, status=403)

        winning_res = get_object_or_404(TradeResponse, id=response_id, trade_offer=offer, status='pending')

        offer_items = InventoryItem.objects.filter(tradeofferitem__trade_offer=offer)
        for item in offer_items:
            item.user = winning_res.responder
            item.status = 'in_inventory'
            item.save()

        res_items = InventoryItem.objects.filter(traderesponseitem__trade_response=winning_res)
        for item in res_items:
            item.user = offer.creator
            item.status = 'in_inventory'
            item.save()

        # 3. Закрываем Offer и принимаем Response
        offer.status = TradeOffer.StatusChoices.CLOSED
        offer.save()
        winning_res.status = TradeResponse.StatusChoices.ACCEPTED
        winning_res.save()

        # 4. ОТКЛОНЯЕМ ОСТАЛЬНЫЕ ОТВЕТЫ И ВОЗВРАЩАЕМ ИМ ВЕЩИ
        other_responses = offer.responses.filter(status='pending').exclude(id=winning_res.id)
        for other in other_responses:
            other.status = InventoryItem.StatusChoices.IN_INVENTORY
            other.save()
            # Возвращаем вещи владельцам
            other_items = InventoryItem.objects.filter(traderesponseitem__trade_response=other)
            other_items.update(status='in_inventory')
        other_responses.delete()

        return Response({"detail": "The exchange has been completed successfully!"})