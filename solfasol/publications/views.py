import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.files.storage import DefaultStorage
from django.utils import timezone
from solfasol.content.models import Content
from .models import Publication


@login_required
def content_editor(request, content_id=None):
    publication = Publication.objects.filter(
        users=request.user,
    ).first()
    if content_id:
        content = Content.objects.filter(
            id=content_id,
            publication=publication,
        )
    else:
        content = None
    return render(request, 'publications/editor.html', {
        'publication': publication,
        'content': content,
    })


@login_required
def content_save(request):
    publication = Publication.objects.filter(
        users=request.user,
    ).first()
    data = json.loads(request.POST.get('data', ''))
    if request.is_ajax:
        title = None
        for block in data['blocks']:
            if block['type'] == 'header':
                title = block['data']['text']
        document_id = request.POST.get('id')
        if document_id:
            content = Content.objects.get(id=document_id)
            content.body = data
            content.save()
        else:
            content = Content.objects.create(
                title=title,
                body=data,
                publication=publication,
                published_by=request.user,
            )
        return JsonResponse({
            'id': content.id,
            'url': reverse('pub_content_detail', kwargs={
                'publication_slug': publication.slug,
                'content_slug': content.slug,
            }),
        })


@csrf_exempt
@login_required
def image_upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        fs = DefaultStorage()
        now = timezone.now()
        filename = fs.save(
            f'content_images/{now.year}/{now.month}/{now.day}/{image.name}',
            image
        )
        uploaded_file_url = fs.url(filename)
        return JsonResponse({
            'success': 1,
            'file': {
                'url': uploaded_file_url,
            }
        })
    return JsonResponse({
        'success': 0,
    })


def view_content(request, content_slug, publication_slug=None):
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    if not publication:
        publication = get_object_or_404(Publication, slug=publication_slug)
    content = get_object_or_404(Content, publication=publication, slug=content_slug)
    return render(request, 'publications/content.html', {
        'content': content,
    })
