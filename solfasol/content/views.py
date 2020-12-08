from django.views.generic import ListView, DetailView, CreateView
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from solfasol.issues.models import Page
from solfasol.publications.models import Publication
from solfasol.publications.views import content_detail as pub_content_detail, content_list as pub_content_list
from .models import Content, Category, Tag, Contributor, Series


def content_list(request, **kwargs):
    context = {}
    qs = Content.objects.filter(
        publish=True,
        publish_at__lt=now(),
    )
    if kwargs.get('category'):
        qs = qs.filter(category__slug=kwargs.get('category'))
        category = get_object_or_404(Category, slug=kwargs['category'])
        context.update({
            'list_type': _('category'),
            'category': category,
            'title': category.name,
        })
    elif kwargs.get('tag'):
        qs = qs.filter(tags__slug=kwargs.get('tag'))
        tag = get_object_or_404(Tag, slug=kwargs['tag'])
        context.update({
            'list_type': _('tag'),
            'tag': tag,
            'title': tag.name,
            'pages': Page.objects.filter(content__tags=tag),
        })
    elif kwargs.get('series'):
        qs = qs.filter(series__slug=kwargs.get('series'))
        series = get_object_or_404(Series, slug=kwargs['series'])
        context.update({
            'list_type': _('series'),
            'series': series,
            'title': series.name,
        })
    elif kwargs.get('popular'):
        qs = qs.order_by('-view_count')[:20]
        context.update({
            'list_type': _('popular'),
            'title': _('popular'),
        })
    elif kwargs.get('contributor'):
        qs = qs.filter(contributors__slug=kwargs.get('contributor'))
        contributor = get_object_or_404(Contributor, slug=kwargs['contributor'])
        context.update({
            'list_type': _('contributor'),
            'contributor': contributor,
            'title': contributor.name,
            'pages': Page.objects.filter(content__contributors=contributor),
        })
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    if publication:
        qs = qs.filter(publication=publication)
    else:
        qs = qs.filter(publication__isnull=True)
    context.update({
        'content_list': qs.distinct(),
    })
    if publication:
        context.update({
            'publication': publication,
        })
        return pub_content_list(request, context)
    return render(request, 'content/content_list.html', context)


@cache_page(5*60)  # 5 mins
@vary_on_cookie
def content_detail(request, slug):
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    if publication:
        return pub_content_detail(request, publication, slug)

    content = get_object_or_404(Content, slug=slug)
    content.view_count += 1
    content.save()
    return render(request, 'content/content_detail.html', {
        'content': content,
    })
