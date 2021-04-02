from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from solfasol.events.models import Event


def event_list(request):
    now = timezone.now()
    events = Event.objects.filter(
        Q(end__isnull=True, start__gt=now) | Q(end__gt=now)
    )
    return render(request, 'events/event_list.html', {
        'events': events,
    })
