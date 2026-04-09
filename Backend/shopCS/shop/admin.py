from django.contrib import admin

# Register your models here.

from .models import Category,Weapon,Rarity,Wear,Skin, InventoryItem,Cart,CartItem

admin.site.register(Category)
admin.site.register(Weapon)
admin.site.register(InventoryItem)
admin.site.register(Rarity)
admin.site.register(Wear)
admin.site.register(Skin)
admin.site.register(Cart)
admin.site.register(CartItem)