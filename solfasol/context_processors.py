from solfasol.content.models import Category, Content, Article, Video


def generic(request):
    return {
        'categories': Category.objects.all(),
        'popular_content': Content.objects.filter(publish=True).order_by('-view_count')[:6],
        'popular_articles': Article.objects.filter(publish=True).order_by('-view_count')[:6],
        'popular_videos': Video.objects.filter(publish=True).order_by('-view_count')[:6],
    }
