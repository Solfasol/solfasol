from django.contrib import admin
from solfasol.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'end', 'online']
    list_editable = ['online']
