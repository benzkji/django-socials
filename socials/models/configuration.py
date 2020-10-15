import requests

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .. import conf
from .post import Post


class ConfigurationManager(models.Manager):

    def get_latest(self):
        qs = self.get_queryset()
        return qs.first()


class Configuration(models.Model):

    objects = ConfigurationManager()

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

    url = models.URLField(
        blank=True,
        verbose_name=_('Instagram URL'),
    )

    app_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('App ID')
    )
    app_secret = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('App Secret')
    )

    token = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Long-lived access token')
    )
    refresh_date = models.DateTimeField(
        verbose_name=_('Last refresh'),
    )

    class Meta:
        ordering = ['-date_added']
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')

    def __str__(self):
        return '{}'.format(self.name)

    def get_token(self, short_token):
        # TODO finish implementation !!!
        url = '{}access_token'.format(conf.INSTAGRAM_API)
        params = {
            'grant_type': 'ig_exchange_token',
            'client_secret': self.app_secret,
            'access_token': short_token
        }
        req = requests.get(url, params=params)  # NOQA
        # print(req.json())

    def refresh_token(self):
        """
        naive way of refreshing the token
        """
        now = timezone.now()
        limit = now - timedelta(days=20)
        data = {}
        if self.refresh_date < limit:
            url = '{}refresh_access_token'.format(conf.INSTAGRAM_API)
            params = {
                'grant_type': 'ig_refresh_token',
                'access_token': self.token
            }
            req = requests.get(url, params=params)
            data = req.json()
        else:
            print('got a fresch token')
        if data:
            self.token = data.get('access_token')
            self.refresh_date = now
            self.save()
        elif settings.DEBUG:
            print('could not refresh token')

    def get_media(self):
        url = '{}/me/media'.format(conf.INSTAGRAM_API)
        params = {
            'access_token': self.token,
            'fields': (
                'id'
                ',timestamp'
                ',permalink'
                ',media_type'
                ',media_url'
                ',caption'
                ',thumbnail_url'
            ),
        }
        try:
            req = requests.get(url, params=params)
        except Exception as e:
            if conf.settings.DEBUG:
                print(e)
            return
        response = req.json()
        if response.get('data'):
            return response['data']
        elif conf.settings.DEBUG:
            # TODO raise insta exception !!!
            print(response.get('error'))
        return

    def refresh_media(self):
        media = self.get_media() or []
        for m in media:
            postid = int(m['id'])
            obj, created = Post.objects.get_or_create(
                originalid=postid,
                configuration_id=self.id,
            )
            obj.data = m
            if obj.data.get('timestamp'):
                obj.save()

    def get_posts(self, amount=None):
        qs = self.post_set.all()
        if amount:
            qs = qs[:amount]
        return qs
