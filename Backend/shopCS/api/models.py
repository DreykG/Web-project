from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WeaponType(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='weapon_types')

    def __str__(self):
        return self.name


class Skin(models.Model):
    class RarityChoices(models.TextChoices):
        SIMPLE = 'Simple', 'Simple'
        RARE = 'Rare', 'Rare'
        EPIC = 'Epic', 'Epic'
        MYTHICAL = 'Mythical', 'Mythical'
        LEGENDARY = 'Legendary', 'Legendary'

    name = models.CharField(max_length=100)
    weapon_type = models.ForeignKey(WeaponType, on_delete=models.CASCADE, related_name='skins')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rarity = models.CharField(max_length=20, choices=RarityChoices.choices)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.weapon_type} | {self.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)

    def __str__(self):
        return self.user.username


class Inventory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='inventory_items')
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE, related_name='owned_by')
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skin')

    def __str__(self):
        return f"{self.user} - {self.skin}"
    
    


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cart_items')
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE, related_name='in_carts')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skin')

    def __str__(self):
        return f"{self.user} - {self.skin}"