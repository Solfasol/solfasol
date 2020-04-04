from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Content, Article, Video, Contributor, Tag, Category, Series


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'added', 'modified', 'publish', 'published_by', 'featured', 'pinned', 'view_count']
    search_fields = ['title', 'summary', 'tags__name']
    exclude = ['published_by']
    list_editable = ['publish', 'featured']
    list_filter = ['publish', 'added', 'modified', 'featured']
    autocomplete_fields = ['tags', 'category', 'related_content']
    actions = ['publish']

    def publish(self, request, queryset):
        for article in queryset:
            if not article.publish:
                article.publish = True
                article.published_by = request.user
                article.save()
    publish.short_description = _('Publish')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'author', 'added', 'category', 'publish', 'published_by', 'featured', 'pinned', 'view_count']
    search_fields = ['title', 'author', 'summary', 'tags__name']
    exclude = ['published_by']
    list_editable = ['publish', 'featured', 'category']
    list_filter = ['publish', 'added', 'modified', 'featured']
    autocomplete_fields = ['series', 'author', 'photo_credits', 'tags', 'category', 'related_content']
    actions = ['publish']

    def publish(self, request, queryset):
        for article in queryset:
            if not article.publish:
                article.publish = True
                article.published_by = request.user
                article.save()
    publish.short_description = _('Publish')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'host', 'added', 'category', 'publish', 'published_by', 'featured', 'pinned', 'view_count']
    search_fields = ['title', 'host', 'guests', 'summary', 'tags__name']
    exclude = ['published_by']
    list_editable = ['publish', 'featured', 'category']
    list_filter = ['publish', 'added', 'modified', 'featured']
    autocomplete_fields = ['series', 'host', 'guests', 'tags', 'category', 'related_content']
    actions = ['publish']

    def publish(self, request, queryset):
        for article in queryset:
            if not article.publish:
                article.publish = True
                article.published_by = request.user
                article.save()
    publish.short_description = _('Publish')


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
