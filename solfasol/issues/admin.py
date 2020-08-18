import os
from io import BytesIO
from pdf2image import convert_from_path, convert_from_bytes
from django.core.serializers import serialize, deserialize
from django.core.files.base import ContentFile
from django.contrib import admin
from django.conf import settings
from .models import Issue, Page
from solfasol.content.models import Content, ContentContributor
from nested_admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin


class PageInline(admin.TabularInline):
    model = Page
    extra = 0


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'month', 'page_count']
    autocomplete_fields = ['tags']
    #readonly_fields = ['page_count']
    actions = ['create_pages_from_pdf', 'dump_page_data', 'load_page_data', 'delete_pages']
    inlines = [PageInline]
    search_fields = ['name']

    def create_pages_from_pdf(self, request, queryset):
        for issue in queryset:
            if issue.pdf:
                issue.pdf.seek(0)
                images = convert_from_bytes(issue.pdf.read())
            i = 1
            for image in images:
                page = Page.objects.create(
                    issue=issue,
                    number=i,
                )
                page_io = BytesIO()
                image.save(page_io, 'PNG')
                page.image.save(
                    image.filename,
                    ContentFile(page_io.getvalue()),
                )
                i += 1
            issue.page_count = len(images)
            cover_io = BytesIO()
            images[0].save(cover_io, 'PNG')
            issue.cover.save(
                images[0].filename,
                ContentFile(cover_io.getvalue()),
                save=False,
            )
            issue.save()

    def delete_pages(self, request, queryset):
        for issue in queryset:
            for page in issue.page_set.all():
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, page.image.name))
                except FileNotFoundError:
                    pass
                page.delete()
            issue.page_count = None
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, issue.cover.name))
            except FileNotFoundError:
                pass
            issue.cover = None
            issue.save()

    def dump_page_data(self, request, queryset):
        for issue in queryset:
            data = serialize("json", issue.page_set.all())
            with open(f'{issue}-pages.json', 'w') as f:
                f.write(data)

    def load_page_data(self, request, queryset):
        for issue in queryset:
            data = deserialize('json', issue.page_data)
            for page in data:
                page.save()


class ContributorsInline(NestedTabularInline):
    model = ContentContributor
    autocomplete_fields = ['contributor']
    extra = 1


class PageContentInline(NestedStackedInline):
    model = Content
    fields = ['title', 'tags']
    autocomplete_fields = ['tags']
    inlines = [ContributorsInline]
    extra = 1


@admin.register(Page)
class PageAdmin(NestedModelAdmin):
    list_display = ['issue', 'number']
    readonly_fields = ['number']
    inlines = [PageContentInline]
    list_filter = ['issue']
