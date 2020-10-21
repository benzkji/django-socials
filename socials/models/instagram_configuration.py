import requests

from datetime import timedelta, datetime

from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .. import conf
from . import Configuration
from ..utils import parse_to_tags


class InstagramConfiguration(Configuration):

    username = models.CharField(
        max_length=64,
        default='',
        blank=False,
        verbose_name=_('Instagram Username'),
        help_text=_('get posts of one user is possible. no hashtags, no special things. username is only for visual help - the only relevant thing is the token'),
    )
    token = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Long-lived access token'),
        default=''
    )
    token_refresh_date = models.DateTimeField(
        verbose_name=_('Last long-lived token refresh'),
        null=True,
    )
    token_ok = models.BooleanField(
        default=False,
    )
    posts_refresh_date = models.DateTimeField(
        verbose_name=_('Last posts refresh'),
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Instagram Configuration')
        verbose_name_plural = _('Instagram Configurations')

    def __str__(self):
        return '{}'.format(self.name)

    # def get_set_token(self, short_token):
    #     """
    #     not used yet, as we use the token generator
    #     > basic display > scroll down to test users > generate token
    #     :param short_token:
    #     :return:
    #     """
    #     url = '{}access_token'.format(conf.INSTAGRAM_API)
    #     params = {
    #         'grant_type': 'ig_exchange_token',
    #         'client_secret': self.app_secret,
    #         'access_token': short_token
    #     }
    #     response = requests.get(url, params=params)  # NOQA
    #     print(response.json())
    #     """
    #     should return:
    #     {
    #       "access_token": "{access-token}",
    #       "token_type": "{token-type}",
    #       "expires_in": {expires-in}
    #     }
    #     """
    #     if response.status_code == 200:
    #         json = response.json
    #         self.token = json.get('access_token', '')
    #         # self.token_expires = json.get('expires_in', 36000)
    #         self.token_ok = True

    def refresh(self):
        self.refresh_token()
        self.refresh_media()

    def refresh_token(self):
        """
        naive way of refreshing the token
        """
        now = timezone.now()
        limit = now - timedelta(days=20)
        # TODO: use expires_in from response data?
        if self.token_refresh_date < limit:
            url = '{}refresh_access_token'.format(conf.INSTAGRAM_API)
            params = {
                'grant_type': 'ig_refresh_token',
                'access_token': self.token
            }
            response = requests.get(url, params=params)
            data = response.json()
        else:
            print('no need to get a fresch token yet')
            return
        if response.status_code == 200 and data:
            self.token = data.get('access_token')
            self.refresh_date = now
            self.token_ok = True
            self.save()
        elif settings.DEBUG:
            self.token_ok = False
            self.save()
            print('could not refresh token')
            return

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
            response = requests.get(url, params=params)
        except (
            ConnectionRefusedError,
            ConnectionError,
            ConnectionAbortedError,
            ConnectionResetError,
        ) as e:
            if conf.settings.DEBUG:
                print(e)
            return
        if response.status_code == 400:
            # bad request!
            self.token_ok = False
            self.save()
            return
        json = response.json()
        if response.status_code == 200 and json.get('data', None):
            return json['data']
        elif conf.settings.DEBUG:
            print(json.get('error'))
        return

    def refresh_media(self):
        if not self.token_ok:
            return
        media = self.get_media()
        if media is None:
            return
        for m in media:
            post_data = self.get_data_dict(m)
            tags = []
            if conf.ENABLE_TAGS:
                tags = parse_to_tags(m.get('caption', ''))
            post_data['tags'] = tags
            post_data['original_data'] = m
            self.configuration_ptr.persist_post(post_data)
        self.posts_refresh_date = timezone.now()
        self.save()

    def get_data_dict(self, json_data):
        if json_data.get('timestamp', None):
            string = json_data['timestamp']
            date = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S+%f')
        if json_data['media_type'] == 'VIDEO':
            image_url = json_data['thumbnail_url']
        else:  # naive fallback. know at least about "VIDEO"...
            image_url = json_data['media_url']
        return {
            'original_id': truncatechars(json_data.get('id', ''), ''),
            'title': truncatechars(json_data.get('caption', ''), conf.INSTAGRAM_TITLE_TRUNCATE),
            'description': json_data.get('caption', ''),
            'image_url': image_url,
            'date': date,
            'url': json_data.get('permalink', ''),
        }

    def get_posts(self, amount=None):
        qs = self.post_set.all()
        if amount:
            qs = qs[:amount]
        return qs
