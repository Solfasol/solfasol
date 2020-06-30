from slugify import slugify
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from solfasol.contributors.models import Contributor


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)
    related_tags = models.ManyToManyField('self', verbose_name=_('related tags'), blank=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'tag': self.slug})

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class TagDefinition(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('tag'), on_delete=models.CASCADE)
    definition = models.TextField(_('definition'))
    contributor = models.ForeignKey(
        Contributor, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('contributor')
    )
    added = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.tag.name

    class Meta:
        verbose_name = _('tag definition')
        verbose_name_plural = _('tag definitions')


class TagImage(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('tag'), on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to=_('tags/'))
    description = models.CharField(_('description'), max_length=280, blank=True, null=True)
    contributor = models.ForeignKey(
        Contributor, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('contributor')
    )
    added = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.tag.name

    class Meta:
        verbose_name = _('tag image')
        verbose_name_plural = _('tag images')


class TagVideo(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('tag'), on_delete=models.CASCADE)
    video_url = models.URLField(_('video url'), blank=True, null=True)
    description = models.CharField(_('description'), max_length=280, blank=True, null=True)
    contributor = models.ForeignKey(
        Contributor, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('contributor')
    )
    added = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.tag.name

    class Meta:
        verbose_name = _('tag video')
        verbose_name_plural = _('tag videos')


