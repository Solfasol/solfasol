from io import BytesIO
import qrcode
import qrcode.image.svg
from slugify import slugify
from django.http import HttpResponse
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from nested_admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from .models import Content, ContentSection, ContentSectionImage, Contributor, ContentContributor, ContributionType, \
    Tag, Category, Series
from django.db.models import TextField
from ckeditor.widgets import CKEditorWidget


class ContentSectionImageInline(NestedStackedInline):
    model = ContentSectionImage
    extra = 0
    fk_name = 'content_section'


class ContentSectionInline(NestedStackedInline):
    model = ContentSection
    extra = 0
    inlines = [ContentSectionImageInline]
    fk_name = 'content'
    formfield_overrides = {
        TextField: {'widget': CKEditorWidget},
    }


class ContributorsInline(admin.TabularInline):
    model = ContentContributor
    autocomplete_fields = ['contributor']
    inlines = []  # monkey patch nested inlines' bug


@admin.register(Content)
class ContentAdmin(NestedModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'added', 'category', 'publish', 'published_by', 'featured', 'pinned', 'view_count']
    search_fields = ['title', 'summary', 'tags__name']
    exclude = ['published_by']
    list_editable = ['publish', 'featured', 'category', 'pinned']
    list_filter = ['publish', 'added', 'modified', 'featured']
    autocomplete_fields = ['tags', 'category', 'related_content']
    actions = ['publish', 'get_qr']
    inlines = [ContributorsInline, ContentSectionInline]

    def publish(self, request, queryset):
        for article in queryset:
            if not article.publish:
                article.publish = True
                article.published_by = request.user
                article.save()
    publish.short_description = _('Publish')

    def get_qr(self, request, queryset):
        factory = qrcode.image.svg.SvgFragmentImage
        for content in queryset:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=1,
                image_factory=factory,
            )
            qr.add_data(
                'http://solfasol.tv%s' % content.get_absolute_url()
            )
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_buffer = BytesIO()
            img.save(img_buffer)
            img_buffer.seek(0)
            response = HttpResponse(
                img_buffer.read(),
                content_type='image/svg+xml',
            )
            response['Content-Disposition'] = 'attachment; filename="QR-%s.svg"' % slugify(content.slug[:20])
            break
        return response
    get_qr.short_description = _('Get QR code')


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ContributionType)
class ContributionTypeAdmin(admin.ModelAdmin):
    list_display = ['description', 'primary']
    list_editable = ['primary']


@admin.register(ContentContributor)
class ContentContributorAdmin(admin.ModelAdmin):
    list_display = ['content', 'contributor', 'contribution_type']


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
