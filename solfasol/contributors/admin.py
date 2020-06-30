from django.contrib import admin
from .models import Contributor


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'photo', 'twitter', 'instagram']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
