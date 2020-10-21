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
    original_data = JSONField(
        blank=True,
        default=dict,
        verbose_name=_('Original Data'),
    )

    # to add: title / description / image (local image) / image_url / url / original_data (instead of data)
    date = models.DateTimeField(
        verbose_name=_('Post Date'),
        null=True,
    )
    title = models.CharField(
        max_length=128,
        default='',
        blank=True,
        verbose_name=_('Title'),
    )
    description = models.TextField(
        default='',
        blank=True,
        verbose_name=_('Description'),
    )
    image = models.ImageField(
        upload_to='post-images',
        null=True,
        blank=True,
    )
    url = models.URLField(
        max_length=256,
        default='',
        blank=True,
        verbose_name=_('Post URL (permalink)'),
    )
    image_url = models.URLField(
        max_length=512,
        default='',
        blank=True,
        verbose_name=_('Image URL'),
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

    def get_admin_thumbnail(self):
        url = self.image_url
        if url:
            html = '<img style="max-width: 150px" class="socials-thumb" src="{}" alt="">'.format(url)
            return mark_safe(html)
    get_admin_thumbnail.short_description = _('Thumbnail')

    def get_admin_title(self):
        url = self.url
        html = self.title
        if url:
            html += ' <a href="{}" target="_blank">open</a>'.format(url)
        return mark_safe(html)
    get_admin_thumbnail.short_description = _('Thumbnail')
