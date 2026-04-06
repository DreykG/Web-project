from rest_framework import serializers
from .models import Category, WeaponType, Skin, UserProfile, Inventory, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class WeaponTypeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WeaponType
        fields = ['id', 'name', 'category', 'category_id']

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        weapon_type = WeaponType.objects.create(category=category, **validated_data)
        return weapon_type

    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            category_id = validated_data.pop('category_id')
            instance.category = Category.objects.get(id=category_id)

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class SkinSerializer(serializers.ModelSerializer):
    weapon_type = WeaponTypeSerializer(read_only=True)
    weapon_type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Skin
        fields = ['id', 'name', 'weapon_type', 'weapon_type_id', 'price', 'rarity', 'image_url']

    def create(self, validated_data):
        weapon_type_id = validated_data.pop('weapon_type_id')
        weapon_type = WeaponType.objects.get(id=weapon_type_id)
        skin = Skin.objects.create(weapon_type=weapon_type, **validated_data)
        return skin

    def update(self, instance, validated_data):
        if 'weapon_type_id' in validated_data:
            weapon_type_id = validated_data.pop('weapon_type_id')
            instance.weapon_type = WeaponType.objects.get(id=weapon_type_id)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.rarity = validated_data.get('rarity', instance.rarity)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()
        return instance


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    def update(self, instance, validated_data):
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance


class InventorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.user.username', read_only=True)
    skin_id = serializers.IntegerField(source='skin.id', read_only=True)
    skin_name = serializers.CharField(source='skin.name', read_only=True)
    acquired_at = serializers.DateTimeField(read_only=True)


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    skin_id = serializers.IntegerField(write_only=True)
    skin_name = serializers.CharField(source='skin.name', read_only=True)
    price = serializers.DecimalField(source='skin.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'skin_id', 'skin_name', 'price', 'added_at']

    def create(self, validated_data):
        skin_data = validated_data.pop('skin')
        skin = Skin.objects.get(id=skin_data['id'])
        user_profile = self.context['user_profile']
        cart_item = Cart.objects.create(user=user_profile, skin=skin, **validated_data)
        return cart_item