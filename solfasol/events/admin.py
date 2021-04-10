from django.contrib import admin
from solfasol.events.models import Event, EventType


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'start', 'end', 'online', 'active']
    list_editable = ['active']
