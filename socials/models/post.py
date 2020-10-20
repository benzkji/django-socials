from datetime import datetime

from django.db import models
from django.utils.html import mark_safe
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from socials import conf

try:
    # django >= 3
    from django.db.models import JSONField
except Exception:
    # django <= 2.2
    from django.contrib.postgres.fields import JSONField


class Post(models.Model):

    date_added = models.DateTimeField(
        auto_now_add=True,
    )
    date_changed = models.DateTimeField(
        auto_now=True,
    )
    date = models.DateTimeField(
        verbose_name=_('Post Date'),
        null=True,
    )
    published = models.BooleanField(
        default=True,
        verbose_name=_('published/visible'),
    )
    configuration = models.ForeignKey(
        'socials.Configuration',
        null=True,
        on_delete=models.CASCADE,
    )
    original_id = models.CharField(
        max_length=128,
        blank=False,
        verbose_name=_('Original ID'),
    )
    data = JSONField(
        blank=True,
        default=dict,
        verbose_name=_('Original Data'),
    )
    tags = models.ManyToManyField(
        'socials.Tag',
        blank=True,
    )

    class Meta:
        ordering = ['-date']
        unique_together = [
            ['configuration', 'original_id'],
        ]
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return '{}'.format(self.original_id)

    def get_title(self):
        return self.configuration.get_data_dict(self).get('title', '')

    def get_description(self):
        return self.configuration.get_data_dict(self).get('description', '')

    def get_date(self):
        return self.configuration.get_data_dict(self).get('date', '')

    def get_date_str(self):
        date = self.get_date()
        return date.strftime(conf.DATE_FORMAT)
    # get_date_str.short_description = _('Date')

    def get_thumbnail_url(self):
        # TODO clean up this mess
        url = self.data.get('thumbnail_url')
        if not url:
            url = self.data.get('media_url')
        return url or ''

    def get_url(self):
        return self.data.get('permalink') or ''

    def get_admin_thumbnail(self):
        url = self.get_thumbnail_url()
        if url:
            html = '<img style="max-width: 150px" class="socials-thumb" src="{}" alt="">'.format(url)
            return mark_safe(html)
    get_admin_thumbnail.short_description = _('Thumbnail')
