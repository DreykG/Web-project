from rest_framework import serializers
from .models import Cart, CartItem, Category, InventoryItem, Rarity, Skin, Weapon, Wear


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
    inventory_item_detail = InventoryItemSerializer(source="inventory_item", read_only=True)

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