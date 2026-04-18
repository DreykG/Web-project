from rest_framework import serializers
from .models import Case, CaseItem, CaseOpening


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"


class CaseItemSerializer(serializers.ModelSerializer):
    skin_name = serializers.CharField(source="skin.name", read_only=True)
    wear_name = serializers.CharField(source="wear.name", read_only=True)
    url = serializers.CharField(source="skin.url", read_only=True)

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
            "url"
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

class CaseOpenSerializer(serializers.Serializer):
    case_id = serializers.IntegerField()

class LiveDropSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    # user_avatar = serializers.ImageField(source='user.profile.avatar', read_only=True)
    skin_name = serializers.CharField(source='case_item.skin.name', read_only=True)
    skin_image = serializers.ImageField(source='case_item.skin.image', read_only=True)
    case_name = serializers.CharField(source='case.name', read_only=True)
    rarity = serializers.CharField(source='case_item.skin.rarity', read_only=True)

    class Meta:
        model = CaseOpening
        fields = ['id', 
                #   'user_id', 
                  'username',
                #   'user_avatar', 
                  'skin_name', 
                  'skin_image', 
                  'case_name', 
                  'rarity', 
                  'opened_at'
                  ]