from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Gang(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_gang'
    )
    description = models.TextField(blank=True)

    treasury = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (treasure: ${self.treasury})"

    def update_status(self):
        if self.members.count() >= 15:
            self.is_open = False
        else:
            self.is_open = True
        self.save()


class GangMember(models.Model):
    ROLE_CHOICES = (
        (1, 'User'),
        (2, 'Admin'),
        (3, 'Owner'),
    )
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name='members')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='gang_membership'
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-role', 'joined_at']
        verbose_name = "Member of gang"
        verbose_name_plural = "Members of gang"

    def __str__(self):
        return f"{self.user.username} в {self.gang.name} ({self.get_role_display()})"


class GangJoinRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('gang', 'user')


class GangMessage(models.Model):
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"<[{self.user.username}] : {self.text}>"


class GangVaultRental(models.Model):

    RENTAL_STATUS = (
        ('active', 'Active'),      # Юзер сейчас носит предмет
        ('returned', 'Returned'),  # Предмет успешно вернулся в сейф
        ('lost', 'Lost'),          # (На будущее) если юзера кикнули и он не вернул вещь
    )

    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name='rentals')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    item = models.ForeignKey('shop.InventoryItem', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=RENTAL_STATUS, default='active')
    
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = "Return" if self.is_returned else "On hand"
        return f"{self.user.username} took {self.item.skin.name} ({status})"