from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from froala_editor.fields import FroalaField


class Article(models.Model):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(_('subtitle'), max_length=200, blank=True, null=True)

    image = models.ImageField(_('image'), upload_to='articles/', blank=True, null=True)
    video = models.URLField(_('video'), blank=True, null=True)

    summary = models.TextField(_('summary'), blank=True, null=True)
    body = FroalaField(blank=True, null=True)

    author = models.ForeignKey(
        'Contributor', verbose_name=_('author'),
        blank=True, null=True,
        on_delete=models.CASCADE, related_name='article_set'
    )
    photo_credits = models.ManyToManyField(
        'Contributor', verbose_name=_('Photo credits'),
        blank=True, related_name='photographed_articles'
    )

    lang = models.CharField(_('language'), max_length=7, choices=settings.LANGUAGES, default='tr')
    tags = models.ManyToManyField('tag', blank=True)
    category = models.ForeignKey('category', blank=True, null=True, on_delete=models.SET_NULL)
    featured = models.BooleanField(_('featured'), default=False)

    publish = models.BooleanField(_('publish'), default=False)
    published_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    view_count = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ('-added',)


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
    def articles(self):
        return self.article_set.filter(publish=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('order',)
