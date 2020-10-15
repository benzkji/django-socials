from django.conf import settings
from django.utils.translation import ugettext_lazy as _


INSTAGRAM_API = 'https://graph.instagram.com/'


POST_TYPE_CHOICES = getattr(
    settings,
    'SOCIALS_POST_TYPE_CHOICES',
    [
        ('instagram', _('Instagram')),
    ]
)
