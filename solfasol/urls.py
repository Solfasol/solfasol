from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from .content.views import ContentListView, ContentDetailView
from .feedback.views import feedback_form
from .subscriptions.views import subscribe
from .views import IndexView, set_language


urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'mdeditor/', include('mdeditor.urls')),

    path('', IndexView.as_view(), name='index'),

    path('kategori/<slug:category>/', ContentListView.as_view(), name='content_category_list'),
    path('etiket/<slug:tag>/', ContentListView.as_view(), name='content_tag_list'),
    path('kim/<slug:contributor>/', ContentListView.as_view(), name='content_contributor_list'),
    path('populer/', ContentListView.as_view(), {'popular': True}, name='content_popular_list'),

    path('abonelik/', subscribe, name='subscription_form'),

    path('form/<slug:slug>/', feedback_form, name='feedback_form'),
    path('oneri/', RedirectView.as_view(
        pattern_name='feedback_form', permanent=True,
    ), kwargs={'slug': 'program-oneri'}),

    path('<slug:slug>/', ContentDetailView.as_view(), name='content_detail'),

    path('dil/', set_language, name='set_lang'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = 'Solfasol'
admin.site.site_header = _('Solfasol Administration')
admin.site.site_title = _('Solfasol Administration')
