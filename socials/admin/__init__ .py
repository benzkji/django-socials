from django.contrib import admin

from .configuration import Configuration, ConfigurationAdmin
from .post import Post, PostAdmin


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Post, PostAdmin)
