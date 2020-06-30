from io import BytesIO
from django.core.files.base import ContentFile
from pdf2image import convert_from_path, convert_from_bytes
from django.contrib import admin
from .models import Issue, Page


class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    autocomplete_fields = ['tags']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['number', 'date', 'page_count']
    autocomplete_fields = ['tags']
    readonly_fields = ['page_count']
    actions = ['create_pages']
    inlines = [PageInline]

    def create_pages(self, request, queryset):
        for issue in queryset:
            if issue.pdf:
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


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['issue', 'number']
