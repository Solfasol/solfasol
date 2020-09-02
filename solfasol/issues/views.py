from django.views.generic import ListView, DetailView
from django.db.models import Max
from django.shortcuts import get_object_or_404
from .models import Issue, Page


class IssueListView(ListView):
    model = Issue
    context_object_name = 'issue_list'
    template_name = 'issues/issue_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.kwargs.get('year'):
            self.year = self.kwargs.get('year')
        else:
            self.year = Issue.objects.aggregate(Max('year'))['year__max']
        qs = qs.filter(year=self.year)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'selected_year': self.year,
            'issue_years': sorted(list(set(
                Issue.objects.values_list('year', flat=True)
            )), reverse=True),
        })
        return context


class IssueDetailView(DetailView):
    model = Issue
    context_object_name = 'issue'
    template_name = 'issues/issue_detail.html'


class PageDetailView(DetailView):
    model = Page
    context_object_name = 'page'
    template_name = 'issues/page_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Page,
            issue__id=self.kwargs['issue_id'],
            number=self.kwargs['page_no'],
        )
