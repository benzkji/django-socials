from django.contrib import admin

from .configuration import Configuration, ConfigurationAdmin
from .instagram_configuration import InstagramConfiguration, InstagramConfigurationAdmin
from .post import Post, PostAdmin


admin.site.register(InstagramConfiguration, InstagramConfigurationAdmin)
admin.site.register(Post, PostAdmin)
