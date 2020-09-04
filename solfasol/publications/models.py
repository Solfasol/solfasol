from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Publication(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(unique=True)
    editors = models.ManyToManyField(User, verbose_name=_('editors'), related_name='managed_publications')
    writers = models.ManyToManyField(User, verbose_name=_('writers'), related_name='contributed_publications')
