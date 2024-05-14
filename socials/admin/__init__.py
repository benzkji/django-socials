from django.contrib import admin

from ..models import Post
from .instagram_configuration import InstagramConfiguration, InstagramConfigurationAdmin
from .post import PostAdmin

admin.site.register(InstagramConfiguration, InstagramConfigurationAdmin)
admin.site.register(Post, PostAdmin)
