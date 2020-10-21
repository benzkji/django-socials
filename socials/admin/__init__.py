from django.contrib import admin

from .instagram_configuration import InstagramConfiguration, InstagramConfigurationAdmin
from .post import PostAdmin
from ..models import Post


admin.site.register(InstagramConfiguration, InstagramConfigurationAdmin)
admin.site.register(Post, PostAdmin)
