from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from .models import Article, Category, Tag, Contributor


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        qs = super().get_queryset().filter(publish=True)
        if self.kwargs.get('category'):
            qs = qs.filter(category__slug=self.kwargs.get('category'))
        if self.kwargs.get('tag'):
            qs = qs.filter(tags__slug=self.kwargs.get('tag'))
        if self.kwargs.get('author'):
            qs = qs.filter(author__slug=self.kwargs.get('author'))
        if self.kwargs.get('popular'):
            qs = qs.order_by('-view_count')[:20]
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
        elif self.kwargs.get('author'):
            author = get_object_or_404(Contributor, slug=self.kwargs['author'])
            context.update({
                'list_type': _('author'),
                'author': author,
                'title': author.name,
            })
        elif self.kwargs.get('popular'):
            context.update({
                'list_type': _('popular'),
                'title': _('popular'),
            })
        return context


class ArticleDetailView(DetailView):
    model = Article

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)
