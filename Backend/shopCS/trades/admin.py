from django.contrib import admin

from .models import TradeOffer, TradeOfferItem

# Register your models here.
admin.site.register(TradeOffer)
admin.site.register(TradeOfferItem)
