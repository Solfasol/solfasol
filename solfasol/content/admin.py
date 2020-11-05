from io import BytesIO
import qrcode
import qrcode.image.svg
from slugify import slugify
from django.http import HttpResponse
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from nested_admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from .models import Content, ContentSection, ContentSectionImage, ContentContributor, ContributionType, \
    Tag, Category, Series, SeriesContributor
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


class ContributorsInline(NestedTabularInline):
    model = ContentContributor
    autocomplete_fields = ['contributor']


@admin.register(Content)
class ContentAdmin(NestedModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'added', 'publication', 'publish', 'featured', 'pinned', 'view_count']
    search_fields = ['title', 'summary', 'tags__name']
    exclude = [
        'published_by',
    ]
    list_editable = ['publish', 'featured', 'pinned']
    list_filter = ['publish', 'added', 'modified', 'featured']
    autocomplete_fields = [
        'tags',
        'category',
        'related_content',
    ]
    actions = ['publish', 'get_qr']
    inlines = [ContributorsInline, ContentSectionInline]

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            'admin/issue_page_filter.js',
        )

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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        is_publisher = request.user.groups.filter(name='publisher').first()
        if is_publisher:
            qs.filter(publication__users=request.user)
        return qs


@admin.register(ContributionType)
class ContributionTypeAdmin(admin.ModelAdmin):
    list_display = ['description', 'primary']
    list_editable = ['primary']


@admin.register(ContentContributor)
class ContentContributorAdmin(admin.ModelAdmin):
    list_display = ['content', 'contributor', 'contribution_type']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'publication', 'content_count']
    search_fields = ['name', 'publication__site__name']
    prepopulated_fields = {"slug": ("name",)}

    def content_count(self, obj):
        return obj.content_set.count()


class SeriesContentInline(NestedStackedInline):
    model = Content
    fields = ['title', 'tags']
    autocomplete_fields = ['tags']
    inlines = [ContributorsInline]
    extra = 1


class SeriesContributorsInline(NestedTabularInline):
    model = SeriesContributor
    autocomplete_fields = ['contributor']


@admin.register(Series)
class SeriesAdmin(NestedModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = [
        'tags',
        'issues',
    ]
    actions = ['get_qr']
    inlines = [
        SeriesContributorsInline,
        #SeriesContentInline,
    ]

    def get_qr(self, request, queryset):
        factory = qrcode.image.svg.SvgFragmentImage
        for obj in queryset:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=1,
                image_factory=factory,
            )
            qr.add_data(
                'http://solfasol.tv%s' % obj.get_absolute_url()
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
            response['Content-Disposition'] = 'attachment; filename="QR-%s.svg"' % slugify(obj.slug[:20])
            break
        return response
    get_qr.short_description = _('Get QR code')
