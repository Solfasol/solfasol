from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


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

