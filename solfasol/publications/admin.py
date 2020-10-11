from django.contrib import admin
from solfasol.content.models import Category
from .models import Publication, PublicationUser


class PublicationUserInline(admin.TabularInline):
    model = PublicationUser
    autocomplete_fields = ['user']


class CategoryInline(admin.TabularInline):
    model = Category
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['site']
    inlines = [
        PublicationUserInline,
        CategoryInline,
    ]
