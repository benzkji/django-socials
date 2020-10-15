from datetime import datetime

from django.db import models
from django.utils.html import mark_safe
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

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
        verbose_name=_('Date'),
    )
    is_visible = models.BooleanField(
        default=True,
        verbose_name=_('Is visible'),
    )
    configuration = models.ForeignKey(
        'socials.Configuration',
        null=True,
        on_delete=models.CASCADE,
    )
    originalid = models.BigIntegerField(
        blank=True,
        null=True,
        default=None,
        verbose_name=_('Original ID'),
    )
    data = JSONField(
        blank=True,
        default=dict,
        verbose_name=_('Original Data'),
    )

    class Meta:
        ordering = ['-date']
        unique_together = [
            ['configuration', 'originalid'],
        ]
        verbose_name = _('Posts')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return '{}'.format(self.originalid)

    def save(self, **kwargs):
        self.date = self.get_date()
        super().save(**kwargs)

    def get_caption(self):
        return self.data.get('caption', '')

    def get_date(self):
        if self.data.get('timestamp'):
            string = self.data['timestamp']
            # TODO set that in conf
            format = '%Y-%m-%dT%H:%M:%S+%f'
            return datetime.strptime(string, format)
        else:
            return now()

    def get_date_str(self):
        date = self.get_date()
        return date.strftime('%d.%m.%Y')
    get_date_str.short_description = _('Date')

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
            html = '<img class="socials-thumb" src="{}" alt="">'.format(url)
            return mark_safe(html)
    get_admin_thumbnail.short_description = _('Thumbnail')
