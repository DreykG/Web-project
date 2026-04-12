from decimal import Decimal
from django.conf import settings

from django.db import models

user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inventory_items"
    )


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Weapon(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="weapons"
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("category", "name")

    def __str__(self):
        return self.name


class Rarity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Wear(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Skin(models.Model):
    weapon = models.ForeignKey(
        Weapon,
        on_delete=models.CASCADE,
        related_name="skins"
    )
    rarity = models.ForeignKey(
        Rarity,
        on_delete=models.PROTECT,
        related_name="skins"
    )
    base_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    name = models.CharField(max_length=150)
    url = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ("weapon", "name")

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    class StatusChoices(models.TextChoices):
        IN_INVENTORY = "in_inventory", "In inventory"
        ON_SALE = "on_sale", "On sale"
        IN_CART = "in_cart", "In cart"
        IN_TRADE = "in_trade", "In trade"
        # SOLD = "sold", "Sold"
        IN_GANG = "in_gang", "In gang"
        RENTED_FROM_GANG = "rented_from_gang", "Rented from gang"
        

    class ObtainedTypeChoices(models.TextChoices):
        PURCHASED = "purchased", "Purchased"
        CASE_OPENED = "case_opened", "Case opened"
        RECEIVED = "received", "Received"
        BONUS = "bonus", "Bonus"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inventory_items"
    )
    
    skin = models.ForeignKey(
        Skin,
        on_delete=models.CASCADE,
        related_name="inventory_items"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )
    status = models.CharField(
        max_length=30,
        choices=StatusChoices.choices,
        default=StatusChoices.IN_INVENTORY
    )
    obtained_type = models.CharField(
        max_length=30,
        choices=ObtainedTypeChoices.choices,
        default=ObtainedTypeChoices.PURCHASED
    )
    wear = models.ForeignKey(
        Wear,
        on_delete=models.PROTECT,
        related_name="inventory_items"
    )
    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )
    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skin.name} ({self.user.username})"


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "inventory_item")

    def __str__(self):
        return f"{self.inventory_item} in cart #{self.cart.id}"