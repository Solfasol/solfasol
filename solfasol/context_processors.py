from datetime import timedelta
from django.utils import timezone
from solfasol.content.models import Category, Content


def generic(request):
    return {
        'categories': Category.objects.all(),
        'popular_content': Content.objects.filter(
            publish=True,
            publish_at__lt=timezone.now(),
    ).filter(
            added__gt=timezone.now()-timedelta(days=30)
        ).order_by('-view_count')[:6],
    }
