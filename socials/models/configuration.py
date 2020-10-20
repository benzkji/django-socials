from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .. import conf
from .tag import Tag
from .post import Post


class Configuration(models.Model):

    active = models.BooleanField(
        default=True,
    )
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

    def get_data_dict(self, post):
        data_dict = None
        if self.instagramconfiguration:
            data_dict = self.instagramconfiguration.get_data_dict(post)
        if data_dict:
            return data_dict
        return {}

    def persist_post(self, post_data):
        original_id = post_data.get('original_id', None)
        if (original_id):
            post, created = Post.objects.get_or_create(
                original_id=original_id,
                configuration=self,
            )
            post.original_data = post_data['data']
            post.date = self.get_data_dict(post).get('date', timezone.now())
            # print(self.get_data_dict(post).get('date'))
            post.save()
            if conf.ENABLE_TAGS:
                tags = []
                for tag_name in post_data.get('tags', []):
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                    )
                    tags.append(tag)
                post.tags.set(tags)
