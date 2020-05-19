from django.contrib import admin
from .models import Item, Cart, CartItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available']
    list_editable = ['price', 'available']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session', 'item_names']

    def item_names(self, obj):
        return '; '.join(list(obj.items.all()))


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'item', 'paid']
    list_editable = ['paid']
