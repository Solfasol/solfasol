from urllib.parse import urlparse, parse_qs
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from polymorphic.models import PolymorphicModel
from martor.models import MartorField


class Content(PolymorphicModel):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(_('subtitle'), max_length=200, blank=True, null=True)
    lang = models.CharField(_('language'), max_length=7, choices=settings.LANGUAGES, default='tr')
    tags = models.ManyToManyField('tag', blank=True)
    category = models.ForeignKey('category', blank=True, null=True, on_delete=models.SET_NULL)
    series = models.ForeignKey('series', verbose_name=_('series'), blank=True, null=True, on_delete=models.SET_NULL)

    image = models.ImageField(_('image'), upload_to='content/', blank=True, null=True)

    related_content = models.ManyToManyField('self', verbose_name=_('related content'), blank=True)

    publish = models.BooleanField(_('publish'), default=False)
    published_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    featured = models.BooleanField(_('featured'), default=False)

    added = models.DateTimeField(_('date'), default=now)
    modified = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    @cached_property
    def similar_content(self):
        return self.related_content.filter(publish=True)

    class Meta:
        verbose_name = _('content')
        verbose_name_plural = _('content')
        ordering = ('-added',)


class Article(Content):
    summary = models.TextField(_('summary'), blank=True, null=True)
    body = MartorField()

    author = models.ForeignKey(
        'Contributor', verbose_name=_('author'),
        blank=True, null=True,
        on_delete=models.CASCADE, related_name='article_set'
    )
    photo_credits = models.ManyToManyField(
        'Contributor', verbose_name=_('Photo credits'),
        blank=True, related_name='photographed_articles'
    )

    issue = models.PositiveSmallIntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    @cached_property
    def owner(self):
        return self.author

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')


class Video(Content):
    url = models.URLField(_('video url'))

    summary = models.TextField(_('summary'), blank=True, null=True)
    transcript = MartorField(blank=True, null=True)
    podcast = models.URLField(_('podcast url'), blank=True, null=True)

    host = models.ForeignKey(
        'Contributor', verbose_name=_('author'),
        blank=True, null=True,
        on_delete=models.CASCADE, related_name='hosted_video_set'
    )
    guests = models.ManyToManyField(
        'Contributor', verbose_name=_('guests'),
        blank=True,
    )

    def clean(self):
        if 'youtube.com' in self.url:
            if 'watch?v=' in self.url:
                parts = urlparse(self.url)
                params = parse_qs(parts.query)
                v = params.get('v')
                if v:
                    self.url = f"https://youtube.com/embed/{v[0]}"
                else:
                    raise ValidationError(_('Invalid Youtube video link!'))
        else:
            raise ValidationError(_('Please submit a Youtube video link!'))

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    @cached_property
    def owner(self):
        return self.host

    class Meta:
        verbose_name = _('video content')
        verbose_name_plural = _('video content')


class Contributor(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(upload_to='contributor/', blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('contributor')
        verbose_name_plural = _('contributors')


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def content(self):
        return self.content_set.filter(publish=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('order',)


class Series(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    @property
    def content(self):
        return self.content_set.filter(publish=True)

    class Meta:
        verbose_name = _('series')
        verbose_name_plural = _('series')