from django.contrib import admin
from nested_admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from .models import Item, ItemAlternative, Category, Tag, Cart, CartItem


class ItemAlternativeInline(NestedTabularInline):
    model = ItemAlternative
    extra = 0


class ItemInline(NestedTabularInline):
    model = Item
    autocomplete_fields = ['category', 'tags']
    extra = 0
    inlines = [ItemAlternativeInline]


@admin.register(Category)
class CategoryAdmin(NestedModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [ItemInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available']
    list_editable = ['price', 'available']
    autocomplete_fields = ['category', 'tags']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session', 'item_names']

    def item_names(self, obj):
        return '; '.join(list(obj.items.all()))


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'item', 'paid']
    list_editable = ['paid']
