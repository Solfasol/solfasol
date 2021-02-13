import csv
from io import StringIO
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import Subscription, SubscriptionType


@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'description', 'payment_link', 'image']
    list_editable = ['amount', 'description', 'payment_link', 'image']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type_value', 'sub_type', 'email', 'phone',  'renewal', 'created']
    list_editable = ['sub_type']

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for s in qs:
            writer.writerow([
                s.name,
                s.get_type_display(),
                s.email,
                s.phone,
                s.created.strftime('%Y-%m-%d %H:%M'),
                s.reneval and 'Evet' or 'Hayır',
                s.notes,
            ])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="abonelikler.csv"'
        return response
    download.short_description = _('Download')

    def type_value(self, obj):
        return obj.type