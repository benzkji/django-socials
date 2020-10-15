from cms.plugin_pool import plugin_pool

from .instagram import InstagramPlugin


plugin_pool.register_plugin(InstagramPlugin)
