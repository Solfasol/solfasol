from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Article, Contributor, Tag, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'author', 'added', 'modified', 'publish', 'published_by', 'featured', 'view_count']
    search_fields = ['title', 'author', 'summary', 'tags__name']
    exclude = ['published_by']
    list_editable = ['featured']
    list_filter = ['publish', 'added', 'modified', 'featured']
    autocomplete_fields = ['author', 'photo_credits', 'tags', 'category', 'related_articles']
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
