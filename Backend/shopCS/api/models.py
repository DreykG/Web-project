from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


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
    name = models.CharField(max_length=150)
    url = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ("weapon", "name")

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    class StatusChoices(models.TextChoices):
        IN_INVENTORY = "in_inventory", "In inventory"
        IN_CART = "in_cart", "In cart"
        IN_TRADE = "in_trade", "In trade"
        SOLD = "sold", "Sold"
        WITHDRAWN = "withdrawn", "Withdrawn"

    class ObtainedTypeChoices(models.TextChoices):
        PURCHASED = "purchased", "Purchased"
        CASE_OPENED = "case_opened", "Case opened"
        RECEIVED = "received", "Received"
        BONUS = "bonus", "Bonus"

    user = models.ForeignKey(
        User,
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"


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


class Case(models.Model):
    name = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    img_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CaseItem(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="case_items"
    )
    skin = models.ForeignKey(
        Skin,
        on_delete=models.CASCADE,
        related_name="case_items"
    )
    wear = models.ForeignKey(
        Wear,
        on_delete=models.PROTECT,
        related_name="case_items"
    )
    drop_chance = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("case", "skin", "wear")

    def __str__(self):
        return f"{self.case.name} -> {self.skin.name} ({self.wear.name})"


class CaseOpening(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="case_openings"
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="openings"
    )
    case_item = models.ForeignKey(
        CaseItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="openings"
    )
    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="case_openings"
    )
    spent_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )
    opened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} opened {self.case.name}"
    
class TradeOffer(models.Model):
    class StatusChoices(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_trade_offers"
    )
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"TradeOffer #{self.id} by {self.creator}"


class TradeOfferItem(models.Model):
    trade_offer = models.ForeignKey(
        TradeOffer,
        on_delete=models.CASCADE,
        related_name="offer_items"
    )
    inventory_item = models.ForeignKey(
        "InventoryItem",
        on_delete=models.CASCADE,
        related_name="trade_offer_items"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trade_offer", "inventory_item")

    def __str__(self):
        return f"Offer #{self.trade_offer.id} - Item #{self.inventory_item.id}"


class TradeResponse(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    trade_offer = models.ForeignKey(
        TradeOffer,
        on_delete=models.CASCADE,
        related_name="responses"
    )
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trade_responses"
    )
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    creator_approved = models.BooleanField(default=False)
    responder_approved = models.BooleanField(default=False)
    responded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("trade_offer", "responder")

    def __str__(self):
        return f"Response #{self.id} to Offer #{self.trade_offer.id}"


class TradeResponseItem(models.Model):
    trade_response = models.ForeignKey(
        TradeResponse,
        on_delete=models.CASCADE,
        related_name="response_items"
    )
    inventory_item = models.ForeignKey(
        "InventoryItem",
        on_delete=models.CASCADE,
        related_name="trade_response_items"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trade_response", "inventory_item")

    def __str__(self):
        return f"Response #{self.trade_response.id} - Item #{self.inventory_item.id}"


class TradeTransaction(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    trade_offer = models.ForeignKey(
        TradeOffer,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    trade_response = models.ForeignKey(
        TradeResponse,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trade_transactions_as_user1"
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trade_transactions_as_user2"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TradeTransaction #{self.id}"