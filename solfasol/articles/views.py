from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Article, Category


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


class ArticleDetailView(DetailView):
    model = Article

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)
