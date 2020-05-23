from solfasol.content.models import Category, Content


def generic(request):
    return {
        'categories': Category.objects.all(),
        'popular_content': Content.objects.filter(publish=True).order_by('-view_count')[:6],
    }
