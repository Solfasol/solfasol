import datetime
import calendar
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from solfasol.tags.models import Tag


def issue_pdf_path(instance, filename):
    return 'issues/%(year)s-%(month)s/solfasol-%(year)s-%(month)s_%(name)s.pdf' % {
        'year': str(instance.year),
        'month': str(instance.month).zfill(2),
        'name': str(instance.name),
    }


def issue_cover_image_path(instance, filename):
    return 'issues/%(year)s-%(month)s/solfasol-%(year)s-%(month)s_%(name)s-cover.png' % {
        'year': str(instance.year),
        'month': str(instance.month).zfill(2),
        'name': str(instance.name),
    }


def page_image_path(instance, filename):
    return 'issues/%(issue_year)s-%(issue_month)s' \
           '/solfasol-%(issue_year)s-%(issue_month)s_%(issue_name)s-%(page_no)s.png' % {
        'issue_year': str(instance.issue.year),
        'issue_month': str(instance.issue.month).zfill(2),
        'issue_name': str(instance.issue.name),
        'page_no': str(instance.number).zfill(2),
    }


class Issue(models.Model):
    year = models.PositiveSmallIntegerField(_('year'),
        choices=[(r, r) for r in range(2011, datetime.date.today().year + 1)]
    )
    month = models.PositiveSmallIntegerField(_('month'),
        choices=list(((k, v) for k,v in enumerate(calendar.month_name)))[1:]
    )
    name = models.CharField(_('name / number'), max_length=50)
    pdf = models.FileField('PDF', upload_to=issue_pdf_path, blank=True, null=True)
    cover = models.ImageField(_('cover'), upload_to=issue_cover_image_path, blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)
    page_count = models.PositiveSmallIntegerField(_('page count'), blank=True, null=True)

    class Meta:
        ordering = ('-year', '-month')
        verbose_name = _('issue')
        verbose_name_plural = _('issues')

    def __str__(self):
        return str(f'{self.get_month_display()} {self.year} - {self.name}')

    def save(self, **kwargs):
        try:
            self.name = str(int(self.name)).zfill(3)
        except ValueError:
            pass
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('issue_detail', kwargs={'pk': self.id})


class Page(models.Model):
    issue = models.ForeignKey(Issue, verbose_name=_('issue'), on_delete=models.CASCADE)
    number = models.PositiveIntegerField(_('number'))
    image = models.ImageField('image', upload_to=page_image_path, blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)

    def __str__(self):
        return '%s - %s' % (str(self.issue), self.number)

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={
            'issue_id': self.issue.id,
            'page_no': self.number,
        })

    def next(self):
        return self.issue.page_set.filter(id__gt=self.id).first()

    def prev(self):
        return self.issue.page_set.filter(id__lt=self.id).first()

    class Meta:
        ordering = ('number',)
        verbose_name = _('page')
        verbose_name_plural = _('pages')
