from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .articles.views import ArticleDetailView, ArticleListView
from .views import IndexView, set_language


urlpatterns = [
    path('admin/', admin.site.urls),

    path('froala_editor/',include('froala_editor.urls')),

    path('', IndexView.as_view(), name='index'),

    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('kategori/<slug:category>/', ArticleListView.as_view(), name='article_category_list'),
    path('etiket/<slug:tag>/', ArticleListView.as_view(), name='article_tag_list'),
    path('yazar/<slug:author>/', ArticleListView.as_view(), name='article_author_list'),
    path('populer/', ArticleListView.as_view(), {'popular': True}, name='article_popular_list'),

    path('dil/', set_language, name='set_lang'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = 'Solfasol'
admin.site.site_header = _('Solfasol Administration')
admin.site.site_title = _('Solfasol Administration')
