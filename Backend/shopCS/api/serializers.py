from rest_framework import serializers

from .models import (
    Category,
    Weapon,
    Rarity,
    Wear,
    Skin,
    InventoryItem,
    Cart,
    CartItem,
    Case,
    CaseItem,
    CaseOpening,
    TradeOffer,
    TradeOfferItem,
    TradeResponse,
    TradeResponseItem,
    TradeTransaction,
)


# -----------------------------
# BASIC MODEL SERIALIZERS
# -----------------------------

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = "__all__"


class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rarity
        fields = "__all__"


class WearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wear
        fields = "__all__"


class SkinSerializer(serializers.ModelSerializer):
    weapon_name = serializers.CharField(source="weapon.name", read_only=True)
    rarity_name = serializers.CharField(source="rarity.name", read_only=True)

    class Meta:
        model = Skin
        fileds = [
            "id",
            "name"
            "weapon"
            "weapon_name"
            "rarity"
            "rarity_name"
            "url"
        ]


class InventoryItemSerializer(serializers.ModelSerializer):
    skin_name = serializers.CharField(source="skin.name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    wear_name = serializers.CharField(source="wear.name", read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "user",
            "user_username",
            "skin",
            "skin_name",
            "price",
            "status",
            "obtained_type",
            "wear",
            "wear_name",
            "purchase_price",
            "sale_price",
            "created_at",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    inventory_item_detail = InventoryItemSerializer(sorce="inventory_item", read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "inventory_item",
            "inventory_item_detail",
            "added_at"
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "items",
        ]


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"


class CaseItemSerializer(serializers.ModelSerializer):
    skin_name = serializers.CharField(source="skin.name", read_only=True)
    wear_name = serializers.CharField(source="wear.name", read_only=True)

    class Meta:
        model = CaseItem
        fields = [
            "id",
            "case",
            "skin",
            "skin_name",
            "wear",
            "wear_name",
            "drop_chance",
            "created_at",
        ]


class CaseOpeningSerializer(serializers.ModelSerializer):
    case_name = serializers.CharField(source="case.name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = CaseOpening
        fields = [
            "id",
            "user",
            "user_username",
            "case",
            "case_name",
            "case_item",
            "inventory_item",
            "spent_balance",
            "opened_at",
        ]


# -----------------------------
# TRADE MODEL SERIALIZERS
# -----------------------------

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


class CaseOpenSerializer(serializers.Serializer):
    case_id = serializers.IntegerField()