from django.db import models
from django.utils.translation import ugettext_lazy as _


class FeedbackForm(models.Model):
    title = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    embed_url = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('feedback form')
        verbose_name_plural = _('feedback forms')
