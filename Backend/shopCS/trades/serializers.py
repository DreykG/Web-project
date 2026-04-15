from rest_framework import serializers
from .models import TradeOffer, TradeOfferItem, TradeResponse, TradeResponseItem
from shop.serializers import InventoryItemSerializer
from shop.models import InventoryItem

class TradeOfferItemSerializer(serializers.ModelSerializer):
    inventory_item_details = InventoryItemSerializer(source="inventory_item", read_only=True)
    
    class Meta:
        model = TradeOfferItem
        fields = [
            "id",
            "inventory_item",
            "inventory_item_details",
        ]


class TradeResponseItemSerializer(serializers.ModelSerializer):
    inventory_item_details = InventoryItemSerializer(source="inventory_item", read_only=True)

    class Meta:
        model = TradeResponseItem
        fields = [
            "id",
            "inventory_item",
            "inventory_item_details",
        ]


class TradeResponseSerializer(serializers.ModelSerializer):
    responder_username = serializers.CharField(source='responder.username', read_only=True)
    items = TradeResponseItemSerializer(many=True, source='response_items')

    class Meta:
        model = TradeResponse
        fields = [
            "id", 
            "responder", 
            "responder_username", 
            "status", 
            "response_value", 
            "items", 
            "responded_at"
            ]
        
class TradeOfferSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    items = TradeOfferItemSerializer(many=True, source='offer_items', read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    responses_count = serializers.IntegerField(source='responses.count', read_only=True)
    responses = TradeResponseSerializer(many=True, read_only=True)
    class Meta:
        model = TradeOffer
        fields = [
            "id", "creator", "creator_username", 
            "title", "status", "offer_value", 
            "items", "responses_count", "responses", "created_at", "is_private", "password"
        ]





