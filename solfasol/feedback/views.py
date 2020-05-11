from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import FeedbackForm


def feedback_form(request, slug):
    form = get_object_or_404(FeedbackForm, slug=slug)
    return render(request, 'feedback/form.html', {
        'form': form,
    })
