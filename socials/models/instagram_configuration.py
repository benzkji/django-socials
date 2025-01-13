from datetime import datetime, timedelta
import re
import time
import json

import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .. import conf
from ..utils import parse_to_tags
from . import Configuration


class InstagramConfiguration(Configuration):
    username = models.CharField(
        max_length=64,
        default="",
        blank=False,
        verbose_name=_("Instagram Username"),
        help_text=_(
            "get posts of one user is possible. no hashtags, no special things. "
            "username is only for visual help - the only relevant thing is the token"
        ),
    )
    token = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Long-lived access token"),
        default="",
    )
    token_refresh_date = models.DateTimeField(
        verbose_name=_("Last long-lived token refresh"),
        null=True,
    )
    token_ok = models.BooleanField(
        default=False,
    )
    posts_refresh_date = models.DateTimeField(
        verbose_name=_("Last posts refresh"),
        null=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Instagram Configuration")
        verbose_name_plural = _("Instagram Configurations")

    def __str__(self):
        return "{}".format(self.name)

    def refresh(self):
        self.refresh_media()

    def get_media(self):
        s = requests.Session()
        # s.headers.update({
        #     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        #     "Accept-Language": "en-US,en;q=0.9",
        #     "Cache-Control": "no-cache",
        #     "Pragma": "no-cache",
        # })
        try:
            # url = "{}{}".format(conf.INSTAGRAM_URL, self.username)
            # response1 = s.get(url)
            # matches = re.search('"app_id":"([^"]*)"', response1.text)
            # app_id = matches.group(1)
            # info_url = f"{conf.INSTAGRAM_URL}api/v1/users/web_profile_info/?username={self.username}"
            # time.sleep(2)
            # response = s.get(info_url, headers={"X-App-Id": app_id})
            url = "{}{}/embed/".format(conf.INSTAGRAM_URL, self.username)
            response = s.get(url)
        except (
            ConnectionRefusedError,
            ConnectionError,
            ConnectionAbortedError,
            ConnectionResetError,
        ) as e:
            if conf.DEBUG:
                print(e)  # noqa
            return
        if response.status_code >= 400:
            # bad request!
            self.token_ok = False
            self.save()
            if conf.DEBUG:
                print("error 400 when getting media")  # noqa
            return
        content = response.text
        if response.status_code == 200:
            for line in content.splitlines():
                if re.match('.*"contextJSON":', line):
                    line = re.sub('.*"contextJSON":"', "", line)
                    line = re.sub('"}]],\["NavigationMetrics",.*', "", line)
                    line = line.replace('\\"', '"')
                    data = json.loads(line)
                    data = data.get("context", {}).get("graphql_media", [])
            return data
        elif conf.DEBUG:
            print(json.get("error"))  # noqa
        return

    def refresh_media(self):
        media = self.get_media()
        if media is None:
            return
        for m in media:
            post_data = self.get_data_dict(m)
            tags = []
            if conf.ENABLE_TAGS:
                tags = parse_to_tags(m.get("caption", ""))
            post_data["tags"] = tags
            post_data["original_data"] = m
            self.configuration_ptr.persist_post(post_data)
        self.posts_refresh_date = timezone.now()
        if conf.DEBUG:
            print("refresh media: SUCCESS")  # noqa
        self.save()

    def get_data_dict(self, json_data):
        json_data = json_data["shortcode_media"]
        if json_data.get("taken_at_timestamp", None):
            string = json_data["taken_at_timestamp"]
            # date = datetime.strptime(string, "%Y-%m-%dT%H:%M:%S+%f")
            date = datetime.fromtimestamp(string)
        image_url = json_data["display_url"].replace("\/", "/")
        image = requests.get(image_url)
        image_obj = SimpleUploadedFile(json_data.get("id", "") + ".jpg", image.content)
        text = json_data.get("edge_media_to_caption", "")["edges"][0]["node"]["text"]
        print(f"https://www.instagram.com/p/{json_data.get('shortcode', )}")
        return {
            "original_id": truncatechars(json_data.get("id", ""), ""),
            "title": truncatechars(
                text, conf.INSTAGRAM_TITLE_TRUNCATE
            ),
            "description": text, # json_data.get("edge_media_to_caption", "")["edges"][0]["node"]["text"],
            "image_url": image_url,
            "image": image_obj,
            "date": date,
            "url": f"https://www.instagram.com/p/{json_data.get('shortcode', )}/",
        }

    def get_posts(self, amount=None):
        qs = self.post_set.all()
        if amount:
            qs = qs[:amount]
        return qs

