from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from .content.views import content_list, content_detail
from .feedback.views import feedback_form
from .subscriptions.views import subscribe
from .shop.views import ItemListView, CartDetailView, ItemDetailView, cart_add, cart_remove, payment_form, callback_3d
from .tags.views import tag_detail
from .issues.views import IssueListView, IssueDetailView, PageDetailView
from .publications.views import content_editor, image_upload, content_save
from .views import index, set_language


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('solfasol.publications.urls')),

    path('', index, name='index'),

    path('canli/', TemplateView.as_view(template_name='youtube_live.html'), name='youtube_live'),

    path('kategori/<slug:category>/', content_list, name='content_category_list'),
    path('etiket/<slug:tag>/', content_list, name='content_tag_list'),
    path('dosya/<slug:series>/', content_list, name='content_series_list'),
    path('kim/<slug:contributor>/', content_list, name='content_contributor_list'),
    path('populer/', content_list, {'popular': True}, name='content_popular_list'),

    #path('dizin/', ContentListView.as_view(), name='tag_list'),
    path('dizin/<str:tag_name>/', tag_detail, name='tag_detail'),

    path('arsiv/', IssueListView.as_view(), name='issue_list'),
    path('arsiv/<int:year>/', IssueListView.as_view(), name='issue_list_year'),
    path('arsiv/sayi/<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
    path('arsiv/<int:issue_id>/<int:page_no>/', PageDetailView.as_view(), name='page_detail'),

    path('abonelik/', subscribe, name='subscription_form'),

    path('form/<slug:slug>/', feedback_form, name='feedback_form'),
    path('oneri/', RedirectView.as_view(
        pattern_name='feedback_form', permanent=True,
    ), kwargs={'slug': 'program-oneri'}),

    path('dukkan/', CartDetailView.as_view(), name='cart_detail'),
    path('dukkan/', ItemListView.as_view(), name='shop_item_list'),
    path('dukkan/odeme/', payment_form, name='shop_payment_form'),
    path('dukkan/odeme/3ds/callback', callback_3d, name='shop_3ds_callback'),
    path('dukkan/satis-sozlesmesi/',
         TemplateView.as_view(template_name='shop/sales-agreement.html'),
         name='sales_agreement'),
    path('dukkan/cart/add/item/<int:item_id>/', cart_add, name='cart_add_item'),
    path('dukkan/cart/add/issue/<int:issue_id>/', cart_add, name='cart_add_issue'),
    path('dukkan/cart/remove/item/<int:item_id>/', cart_remove, name='cart_remove_item'),
    path('dukkan/cart/remove/issue/<int:issue_id>/', cart_remove, name='cart_remove_issue'),
    path('dukkan/<slug:slug>/', ItemDetailView.as_view(), name='shop_item_detail'),

    path('dil/', set_language, name='set_lang'),

    path('<slug:slug>/', content_detail, name='content_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = 'Solfasol'
admin.site.site_header = _('Solfasol Administration')
admin.site.site_title = _('Solfasol Administration')
