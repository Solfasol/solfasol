from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from slugify import slugify


class Publication(models.Model):
    slug = models.SlugField(blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='publications/logo/', blank=True, null=True)
    icon = models.ImageField(upload_to='publications/icon/', blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)
    patreon = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(_('about'), blank=True, null=True)
    about_link = models.URLField(blank=True, null=True)
    about_title = models.CharField(max_length=50, blank=True, null=True)

    users = models.ManyToManyField(User, verbose_name=_('users'), through='PublicationUser', blank=True)

    def __str__(self):
        return self.site.name

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.site.name)
        super().save(**kwargs)

    def get_absolute_url(self):
        return self.site.domain


class PublicationUser(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    editor = models.BooleanField(default=False)
