from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,   
        default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    cases_opened_count = models.PositiveIntegerField(default=0)
    
    total_drop_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    inventory_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Профиль {self.user.username}"