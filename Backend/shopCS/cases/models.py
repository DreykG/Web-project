from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


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
        'shop.Skin',
        on_delete=models.CASCADE,
        related_name="case_items"
    )
    wear = models.ForeignKey(
        'shop.Wear',
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
        settings.AUTH_USER_MODEL,
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
        'shop.InventoryItem',
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
    