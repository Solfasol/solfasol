from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Issue, Page


class IssueListView(ListView):
    model = Issue
    context_object_name = 'issue_list'
    template_name = 'issues/issue_list.html'


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
