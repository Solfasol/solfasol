import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext as _
from django.db.utils import IntegrityError
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.files.storage import DefaultStorage
from django.utils import timezone
from slugify import slugify
from solfasol.content.models import Content, Tag, Category
from .models import Publication


@login_required
def content_editor(request, content_id=None):
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    if content_id:
        content = Content.objects.filter(
            id=content_id,
            publication=publication,
        ).first()
    else:
        content = None
    return render(request, 'publications/editor.html', {
        'publication': publication,
        'content': content,
    })


@login_required
def content_save(request):
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    if publication and not request.user in publication.users.all():
        raise Http404
    data = json.loads(request.POST.get('data', ''))
    if request.is_ajax:
        title, image = None, None
        for block in data['blocks']:
            if block['type'] == 'header':
                title = block['data']['text']
            elif block['type'] == 'image':
                image = block['data']['file']['url']
        if not title:
            return JsonResponse({
                'error': _('No title provided'),
            })
        if not image:
            return JsonResponse({
                'error': _('No image provided'),
            })
        publish = request.POST.get('publish') == 'true'
        document_id = request.POST.get('id')
        if document_id:
            content = Content.objects.get(id=document_id)
            content.data = data
            content.image = image
            content.publish = publish
            content.date = request.POST.get('date')
            content.save()
        else:
            try:
                content = Content.objects.create(
                    title=title,
                    image=image,
                    data=data,
                    publication=publication,
                    publish=publish,
                    published_by=request.user,
                    featured=True,
                    date=request.POST.get('date'),
                )
            except IntegrityError:
                return JsonResponse({
                    'error': _('A post with the same title already exists'),
                })
        content.tags.clear()
        tag_names = [
            t.strip()
            for t in request.POST.get('tags', '').split(',')
            if t.strip()
        ]
        for tag_name in tag_names:
            tag, c = Tag.objects.get_or_create(
                slug=slugify(tag_name),
                defaults={
                    'name': tag_name,
                }
            )
            content.tags.add(tag)
        category_name = request.POST.get('category').strip()
        if category_name:
            category, c = Category.objects.get_or_create(
                slug=slugify(category_name),
                publication=publication,
                defaults={
                    'name': category_name,
                }
            )
            content.category = category
            content.save()
        return JsonResponse({
            'id': content.id,
            'url': content.get_absolute_url(),
        })


@csrf_exempt
@login_required
def image_upload(request):
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    if publication and not request.user in publication.users.all():
        raise Http404
    if request.method == 'POST':
        image = request.FILES['image']
        fs = DefaultStorage()
        now = timezone.now()
        image_path = f'publications/{publication.slug}/{now.year}/{now.month}/{now.day}/{image.name}'
        filename = fs.save(
            image_path,
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


def index(request, publication):
    content = Content.objects.filter(
        publication=publication,
        publish=True,
        publish_at__lt=timezone.now(),
    ).order_by('-date')
    return render(request, 'publications/index.html', {
        'publication': publication,
        'recent_content': content[:6],
        'featured_content': content.filter(featured=True)[:6],
    })


def content_list(request, context):
    return render(request, 'publications/content_list.html', context)


def content_detail(request, publication, content_slug):
    content = get_object_or_404(Content, publication=publication, slug=content_slug)
    content.view_count += 1
    content.save()
    return render(request, 'publications/content_detail.html', {
        'publication': publication,
        'content': content,
    })


