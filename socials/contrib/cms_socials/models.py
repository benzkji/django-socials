from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

from socials.models import Post


class SocialFeed(CMSPlugin):

    amount = models.SmallIntegerField(
        default=20,
    )
    configurations = models.ManyToManyField(
        'socials.Configuration',
        null=True,
        verbose_name=_('Source Configurations')
    )
    hash_tags = models.ManyToManyField(
        'socials.Tag',
        null=True,
        verbose_name=_('Hashtags')
    )

    class Meta:
        verbose_name = _('Social Feed')
        verbose_name_plural = _('Social Feeds')

    def __str__(self):
        return _('Social Feed')

    def get_posts(self):
        posts = Post.objects.filter(published=True)
        if self.configurations:
            posts = posts.filter(configuration__in=self.configurations)
        if self.hash_tags:
            posts = posts.filter(tags__in=self.hash_tags)
        return posts
