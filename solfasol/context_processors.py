from solfasol.articles.models import Category, Article


def generic(request):
    return {
        'categories': Category.objects.all(),
        'popular_articles': Article.objects.filter(publish=True).order_by('-view_count')[:6],
    }
