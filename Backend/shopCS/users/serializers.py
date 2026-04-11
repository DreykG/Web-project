from rest_framework import serializers
from .models import Profile
from django.db.models import Sum

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    balance = serializers.DecimalField(source='user.balance', max_digits=12, decimal_places=2, read_only=True)
    date_joined = serializers.DateTimeField(source='user.created_at', read_only=True)

    inventory_value = serializers.SerializerMethodField()

    def get_inventory_value(self, obj):
        # Считаем сумму всех предметов юзера, которые реально лежат в инвентаре

        total = obj.user.inventory_items.filter(
            status='in_inventory'
        ).aggregate(total_base =Sum('skin__base_price'))['total_base']

        return total or 0

    
    class Meta:
        model = Profile
        fields = [
            'username', 
            'balance', 
            'avatar', 
            'cases_opened_count', 
            'total_drop_value', 
            'inventory_value', 
            'date_joined'
        ]