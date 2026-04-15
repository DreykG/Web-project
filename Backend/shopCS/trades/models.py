from django.db import models
from django.conf import settings
from decimal import Decimal

class TradeOffer(models.Model):
    class StatusChoices(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"
        CANCELLED = "cancelled", "Cancelled"

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_trade_offers"
    )

    title = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN
    )
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=255, blank=True, null=True)

    #Sum of all items in each offer
    offer_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Offer #{self.id} by {self.creator.username} ({self.offer_value}$)"


class TradeOfferItem(models.Model):
    trade_offer = models.ForeignKey(TradeOffer, on_delete=models.CASCADE, related_name="offer_items")
    inventory_item = models.ForeignKey('shop.InventoryItem', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("trade_offer", "inventory_item")




class TradeResponse(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    trade_offer = models.ForeignKey(TradeOffer, on_delete=models.CASCADE, related_name="responses")
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    
    # Sum of items, that suggest Responser
    response_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    responded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trade_offer", "responder")


class TradeResponseItem(models.Model):
    trade_response = models.ForeignKey(TradeResponse, on_delete=models.CASCADE, related_name="response_items")
    inventory_item = models.ForeignKey('shop.InventoryItem', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("trade_response", "inventory_item")