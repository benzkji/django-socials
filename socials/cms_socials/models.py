from django.db import models
from django.utils.translation import ugettext_lazy as _


from cms.models import CMSPlugin


# TODO replace with abstract class from conf.py
class Instagram(CMSPlugin):

    title = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name=_('Title'),
    )
    configuration = models.ForeignKey(
        'socials.Configuration',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Configuration')
    )
    button_label = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name=_('Button label'),
    )

    class Meta:
        verbose_name = _('Instagram')
        verbose_name_plural = _('Instagram')

    def __str__(self):
        return '{}'.format(self.title)

    def get_posts(self):
        if self.configuration:
            return self.configuration.get_posts(amount=4)
        return []
