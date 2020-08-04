from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Tag, TagDefinition, TagImage, TagVideo


class TagDefinitionInline(admin.StackedInline):
    model = TagDefinition
    extra = 0


class TagImageInline(admin.StackedInline):
    model = TagImage


class TagVideoInline(admin.StackedInline):
    model = TagVideo


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'content_count', 'definition_count', 'image_count', 'video_count']
    search_fields = ['name', 'slug']
    inlines = [
        TagDefinitionInline,
        TagImageInline,
        TagVideoInline,
    ]
    autocomplete_fields = ['related_tags']

    def content_count(self, obj):
        return obj.content_set.count()
    content_count.short_description = _('content count')

    def definition_count(self, obj):
        return obj.tagdefinition_set.count()
    definition_count.short_description = _('definition count')

    def image_count(self, obj):
        return obj.tagimage_set.count()
    image_count.short_description = _('image count')

    def video_count(self, obj):
        return obj.tagvideo_set.count()
    video_count.short_description = _('video count')
