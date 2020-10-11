from datetime import date
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils import timezone
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect
from solfasol.content.models import Content
from solfasol.issues.models import Issue
from solfasol.publications.models import Publication
from solfasol.publications.views import index as publication_index


ISSUES_THIS_MONTH_TITLES = {
    1: "Ocak'lar",
    2: "Şubat'lar",
    3: "Mart'lar",
    4: "Nisan'lar",
    5: "Mayıs'lar",
    6: "Haziran'lar",
    7: "Temmuz'lar",
    8: "Ağustos'lar",
    9: "Eylül'ler",
    10: "Ekim'ler",
    11: "Kasım'lar",
    12: "Aralık'lar",
}


@cache_page(5*60)  # 5 mins
def index(request):
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    if publication:
        return publication_index(request, publication)

    this_month = date.today().month
    content = Content.objects.filter(
        publish=True,
        publish_at__lt=timezone.now(),
    )
    return render(request, 'index.html', {
        'recent_content': content[:6],
        'featured_content': content.filter(featured=True)[:6],
        'past_issues': {
            'title': ISSUES_THIS_MONTH_TITLES[this_month],
            'issues': Issue.objects.filter(month=this_month).exclude(year=date.today().year),
        }
    })


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
