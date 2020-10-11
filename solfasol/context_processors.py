from datetime import timedelta
from django.utils import timezone
from solfasol.content.models import Category, Content
from solfasol.publications.models import Publication


def generic(request):
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    return {
        'categories': Category.objects.filter(
            publication=publication,
        ),
        'popular_content': Content.objects.filter(
            publication=publication,
            publish=True,
            publish_at__lt=timezone.now(),
    ).filter(
            added__gt=timezone.now()-timedelta(days=30)
        ).order_by('-view_count')[:6],
    }
