from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from .models import Content, Category, Tag, Contributor, Series


class ContentListView(ListView):
    model = Content
    context_object_name = 'content_list'

    def get_queryset(self):
        qs = super().get_queryset().filter(publish=True)
        if self.kwargs.get('category'):
            qs = qs.filter(category__slug=self.kwargs.get('category'))
        elif self.kwargs.get('tag'):
            qs = qs.filter(tags__slug=self.kwargs.get('tag'))
        elif self.kwargs.get('popular'):
            qs = qs.order_by('-view_count')[:20]
        elif self.kwargs.get('series'):
            qs = qs.filter(series__slug=self.kwargs.get('series'))
        elif self.kwargs.get('contributor'):
            qs = qs.filter(
                Q(Article___author__slug=self.kwargs.get('contributor')) |
                Q(Video___host__slug=self.kwargs.get('contributor'))
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('category'):
            category = get_object_or_404(Category,slug=self.kwargs['category'])
            context.update({
                'list_type': _('category'),
                'category': category,
                'title': category.name,
            })
        elif self.kwargs.get('tag'):
            tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
            context.update({
                'list_type': _('tag'),
                'tag': tag,
                'title': tag.name,
            })
        elif self.kwargs.get('popular'):
            context.update({
                'list_type': _('popular'),
                'title': _('popular'),
            })
        elif self.kwargs.get('series'):
            series = get_object_or_404(Series, slug=self.kwargs['series'])
            context.update({
                'list_type': _('series'),
                'series': series,
                'title': series.name,
            })
        elif self.kwargs.get('contributor'):
            contributor = get_object_or_404(Contributor, slug=self.kwargs['contributor'])
            context.update({
                'list_type': _('contributor'),
                'contributor': contributor,
                'title': contributor.name,
            })
        return context


class ContentDetailView(DetailView):
    model = Content
    template_name = 'content/content_detail.html'
    context_object_name = 'content'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        obj.view_count += 1
        obj.save()
        return obj
