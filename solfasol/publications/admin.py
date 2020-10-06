from django.contrib import admin
from .models import Publication, PublicationUser


class PublicationUserInline(admin.TabularInline):
    model = PublicationUser
    autocomplete_fields = ['user']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['site']
    inlines = [PublicationUserInline]
