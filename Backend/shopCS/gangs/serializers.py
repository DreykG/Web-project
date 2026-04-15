from rest_framework import serializers
from .models import Gang, GangMember, GangJoinRequest, GangMessage, GangVaultRental
from django.contrib.auth import get_user_model


class GangMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    role_name = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = GangMember
        fields = ['id', 'user', 'username', 'role', 'role_name', 'joined_at']


class GangMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    formatted_display = serializers.SerializerMethodField()

    class Meta:
        model = GangMessage
        fields = ['id', 'user', 'username', 'text', 'formatted_display', 'created_at']

    def get_formatted_display(self, obj):
        return f"<[{obj.user.username}] : {obj.text}"


class GangJoinRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    gang_name = serializers.CharField(source='gang.name', read_only=True)

    class Meta:
        model = GangJoinRequest
        fields = ['id', 'gang', 'gang_name', 'user', 'username', 'message', 'status', 'created_at']
        read_only_fields = ['status']


class GangVaultRentalSerializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = GangVaultRental
        fields = [
            'id', 'user', 'item', 'item_details', 'deposit_amount', 
            'status', 'status_display', 'created_at', 'returned_at'
        ]
        read_only_fields = ['deposit_amount', 'status', 'returned_at']

    def get_item_details(self, obj):
        # Инфа о скине для фронта
        return {
            "name": obj.item.skin.name,
            "image": obj.item.skin.image.url if obj.item.skin.image else None,
            "rarity": getattr(obj.item.skin, 'rarity', None)
        }


class GangSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Gang
        fields = ['id', 'name', 'description', 'owner_username', 'members_count', 'is_member']

        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True}
        }

    def get_is_member(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.members.filter(user=user).exists()