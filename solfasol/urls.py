from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from .content.views import ContentListView, ContentDetailView
from .feedback.views import feedback_form
from .subscriptions.views import subscribe
from .shop.views import ItemListView, ItemDetailView, cart_add, cart_remove, payment_form, callback_3d
from .tags.views import tag_detail
from .views import IndexView, set_language


urlpatterns = [

    path('admin/', admin.site.urls),

    #path(r'martor/', include('martor.urls')),

    path('', IndexView.as_view(), name='index'),

    path('kategori/<slug:category>/', ContentListView.as_view(), name='content_category_list'),
    path('etiket/<slug:tag>/', ContentListView.as_view(), name='content_tag_list'),
    path('kim/<slug:contributor>/', ContentListView.as_view(), name='content_contributor_list'),
    path('populer/', ContentListView.as_view(), {'popular': True}, name='content_popular_list'),

    #path('dizin/', ContentListView.as_view(), name='tag_list'),
    path('dizin/<str:tag_name>/', tag_detail, name='tag_detail'),

    path('abonelik/', subscribe, name='subscription_form'),

    path('form/<slug:slug>/', feedback_form, name='feedback_form'),
    path('oneri/', RedirectView.as_view(
        pattern_name='feedback_form', permanent=True,
    ), kwargs={'slug': 'program-oneri'}),

    path('dukkan/', ItemListView.as_view(), name='shop_item_list'),
    path('dukkan/odeme/', payment_form, name='shop_payment_form'),
    path('dukkan/odeme/3ds/callback', callback_3d, name='shop_3ds_callback'),
    path('dukkan/satis-sozlesmesi/',
         TemplateView.as_view(template_name='shop/sales-agreement.html'),
         name='sales_agreement'),
    path('dukkan/cart/add/<int:item_id>/', cart_add, name='shop_cart_add'),
    path('dukkan/cart/remove/<int:item_id>/', cart_remove, name='shop_cart_remove'),
    path('dukkan/<slug:slug>/', ItemDetailView.as_view(), name='shop_item_detail'),

    path('dil/', set_language, name='set_lang'),

    path('<slug:slug>/', ContentDetailView.as_view(), name='content_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = 'Solfasol'
admin.site.site_header = _('Solfasol Administration')
admin.site.site_title = _('Solfasol Administration')
