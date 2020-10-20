from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):

    published = models.BooleanField(
        default=True,
    )
    name = models.CharField(
        max_length=64,
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name