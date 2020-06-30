from django.shortcuts import render
from django.shortcuts import get_object_or_404
from solfasol.issues.models import Page
from .models import Tag


def tag_detail(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    content = tag.content_set.all()
    pages = Page.objects.filter(content__in=content).distinct()
    return render(request, 'tags/tag_detail.html', {
        'tag': tag,
        'definitions': tag.tagdefinition_set.filter(publish=True),
        'content_list': content.filter(publish=True)[:3],
        'issues': tag.issue_set.all(),
        'pages': pages,
    })
