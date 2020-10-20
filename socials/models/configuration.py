import requests

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


from .. import conf
from .post import Post

#
# class ConfigurationManager(models.Manager):
#
#     def get_latest(self):
#         qs = self.get_queryset()
#         return qs.first()
#

class Configuration(models.Model):

    date_added = models.DateTimeField(
        auto_now_add=True,
    )
    date_changed = models.DateTimeField(
        auto_now=True,
    )
    name = models.CharField(
        max_length=255,
        default='',
        verbose_name=_('Name'),
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')

    def __str__(self):
        return '{}'.format(self.name)