from rest_framework import serializers

from Backend.shopCS.shop.serializers import InventoryItemSerializer
from Backend.shopCS.trades.models import TradeOffer, TradeOfferItem, TradeResponse, TradeResponseItem, TradeTransaction
class TradeOfferItemSerializer(serializers.ModelSerializer):
    inventory_item_detail = InventoryItemSerializer(source="inventory_item", read_only=True)

    class Meta:
        model = TradeOfferItem
        fields = [
            "id",
            "trade_offer",
            "inventory_item",
            "inventory_item_detail",
            "created_at",
        ]


class TradeOfferSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source="creator.username", read_only=True)
    offer_items = TradeOfferItemSerializer(many=True, read_only=True)

    class Meta:
        model = TradeOffer
        fields = [
            "id",
            "creator",
            "creator_username",
            "title",
            "message",
            "status",
            "created_at",
            "updated_at",
            "expires_at",
            "offer_items",
        ]


class TradeResponseItemSerializer(serializers.ModelSerializer):
    inventory_item_detail = InventoryItemSerializer(source="inventory_item", read_only=True)

    class Meta:
        model = TradeResponseItem
        fields = [
            "id",
            "trade_response",
            "inventory_item",
            "inventory_item_detail",
            "created_at",
        ]


class TradeResponseSerializer(serializers.ModelSerializer):
    responder_username = serializers.CharField(source="responder.username", read_only=True)
    response_items = TradeResponseItemSerializer(many=True, read_only=True)

    class Meta:
        model = TradeResponse
        fields = [
            "id",
            "trade_offer",
            "responder",
            "responder_username",
            "message",
            "status",
            "creator_approved",
            "responder_approved",
            "responded_at",
            "updated_at",
            "response_items",
        ]


class TradeTransactionSerializer(serializers.ModelSerializer):
    user1_username = serializers.CharField(source="user1.username", read_only=True)
    user2_username = serializers.CharField(source="user2.username", read_only=True)

    class Meta:
        model = TradeTransaction
        fields = [
            "id",
            "trade_offer",
            "trade_response",
            "user1",
            "user1_username",
            "user2",
            "user2_username",
            "status",
            "completed_at",
            "created_at",
        ]


# -----------------------------
# ORDINARY SERIALIZERS
# -----------------------------

class TradeOfferCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    message = serializers.CharField(required=False, allow_blank=True)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    inventory_item_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class TradeResponseCreateSerializer(serializers.Serializer):
    trade_offer_id = serializers.IntegerField()
    message = serializers.CharField(required=False, allow_blank=True)
    inventory_item_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class TradeApproveSerializer(serializers.Serializer):
    creator_approved = serializers.BooleanField(required=False)
    responder_approved = serializers.BooleanField(required=False)
