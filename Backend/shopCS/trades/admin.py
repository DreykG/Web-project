from django.contrib import admin

from .models import TradeOffer, TradeOfferItem, TradeResponse, TradeResponseItem

# Register your models here.
admin.site.register(TradeOffer)
admin.site.register(TradeOfferItem)
admin.site.register(TradeResponse)
admin.site.register(TradeResponseItem)
