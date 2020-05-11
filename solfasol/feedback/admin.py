from django.contrib import admin
from .models import FeedbackForm


@admin.register(FeedbackForm)
class FeedbackFormAdmin(admin.ModelAdmin):
    list_display = ['title', 'embed_url']
    prepopulated_fields = {"slug": ("title",)}
