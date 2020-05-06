from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'type_value']

    def type_value(self, obj):
        return obj.type