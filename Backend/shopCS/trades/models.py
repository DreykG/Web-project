from decimal import Decimal

from django.db import models
from django.conf import settings

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
        'shop.InventoryItem',
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
        'shop.InventoryItem',
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