from django.views.generic import TemplateView, CreateView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from solfasol.content.models import Content


@method_decorator(cache_page(5*60), name='dispatch')  # 5 mins
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content = Content.objects.filter(publish=True)
        context.update({
            'recent_content': content[:6],
            'featured_content': content.filter(featured=True)[:6],
        })
        return context


class SearchResultView(TemplateView):
    template_name = 'search_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        q = self.request.GET.get('q')
        context.update({
        })
        return context


def set_language(request):
    next_page = request.META.get('HTTP_REFERER')
    response = HttpResponseRedirect(next_page) if next_page else HttpResponseRedirect('/')
    lang_code = request.GET.get('lang')
    next_trans = translate_url(next_page, lang_code)
    if next_trans != next_page:
        response = HttpResponseRedirect(next_trans)
    if hasattr(request, 'session'):
        request.session[LANGUAGE_SESSION_KEY] = lang_code
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, lang_code,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
    )
    return response
