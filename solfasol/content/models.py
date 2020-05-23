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
from mdeditor.fields import MDTextField


class Content(PolymorphicModel):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(_('subtitle'), max_length=200, blank=True, null=True)
    contributors = models.ManyToManyField(
        'Contributor',
        verbose_name=_('contributor'),
        blank=True,
        related_name='content_set',
        through='ContentContributor',
    )
    lang = models.CharField(_('language'), max_length=7, choices=settings.LANGUAGES, default='tr')
    tags = models.ManyToManyField('tag', verbose_name=_('tags'), blank=True)
    category = models.ForeignKey('category', verbose_name=_('category'), blank=True, null=True, on_delete=models.SET_NULL)
    series = models.ForeignKey('series', verbose_name=_('series'), blank=True, null=True, on_delete=models.SET_NULL)
    issue = models.PositiveSmallIntegerField(blank=True, null=True)

    image = models.ImageField(_('image'), upload_to='content/')

    video_url = models.URLField(_('video url'), blank=True, null=True)
    podcast = models.URLField(_('podcast url'), blank=True, null=True)

    summary = models.TextField(_('summary'), blank=True, null=True)
    body = MDTextField(_('text body'), blank=True, null=True)

    related_content = models.ManyToManyField('self', verbose_name=_('related content'), blank=True)

    publish = models.BooleanField(_('publish'), default=False)
    published_by = models.ForeignKey(
        User, verbose_name=_('published by'),
        blank=True, null=True,
        on_delete=models.CASCADE,
    )

    featured = models.BooleanField(_('featured'), default=False)
    pinned = models.BooleanField(_('pinned'), default=False)

    added = models.DateTimeField(_('date'), default=now)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    view_count = models.PositiveIntegerField(default=0, editable=False)

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.pinned:
            Content.objects.filter(pinned=True).exclude(id=self.id).update(pinned=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('content_detail', kwargs={'slug': self.slug})

    @cached_property
    def owners(self):
        return ContentContributor.objects.filter(
            content=self,
            contribution_type__primary=True,
        )

    @cached_property
    def similar_content(self):
        return self.related_content.filter(publish=True)

    class Meta:
        verbose_name = _('content')
        verbose_name_plural = _('content')
        ordering = ('-pinned', '-added',)


class Article(Content):
    issue_x = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')


class Video(Content):
    video_url_x = models.URLField(_('video url'))
    podcast_x = models.URLField(_('podcast url'), blank=True, null=True)

    def clean(self):
        if not 'youtube.com/embed/' in self.video_url:
            if 'youtube.com/' or 'youtu.be/' in self.video_url:
                vid = None
                if 'youtube.com/' in self.video_url:
                    if 'watch?v=' in self.video_url:
                        parts = urlparse(self.video_url)
                        params = parse_qs(parts.query)
                        vid = params.get('v', [])[0]
                elif 'youtu.be/' in self.video_url:
                    vid = self.video_url.split('/')[-1]
                if vid:
                    self.video_url = f"https://youtube.com/embed/{vid}"
                else:
                    raise ValidationError(_('Invalid Youtube video link!'))
            else:
                raise ValidationError(_('Please submit a Youtube video link!'))

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

    def get_absolute_url(self):
        return reverse('content_contributor_list', kwargs={'contributor': self.slug})

    class Meta:
        verbose_name = _('contributor')
        verbose_name_plural = _('contributors')


class ContributionType(models.Model):
    description = models.CharField(_('description'), max_length=20)
    primary = models.BooleanField(_('primary'), default=False)

    def __str__(self):
        return self.description


class ContentContributor(models.Model):
    content = models.ForeignKey(Content, verbose_name=_('content'), on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, verbose_name=_('contributor'), on_delete=models.CASCADE)
    contribution_type = models.ForeignKey(
        ContributionType,
        verbose_name=_('contribution type'),
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )

    def __str__(self):
        return self.contributor.name


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('content_tag_list', kwargs={'tag': self.slug})

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('content_category_list', kwargs={'category': self.slug})

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
    category = models.ForeignKey(
        Category, verbose_name=_('category'),
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('content_series_list', kwargs={'series': self.slug})

    @property
    def content(self):
        return self.content_set.filter(publish=True)

    class Meta:
        verbose_name = _('series')
        verbose_name_plural = _('series')
