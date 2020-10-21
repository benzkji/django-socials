from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import SocialFeed


@plugin_pool.register_plugin
class SocialFeedPlugin(CMSPluginBase):

    model = SocialFeed
    module = _('Social')
    name = _('Social Feed')
    render_template = 'socials/plugins/social_feed.html'
    text_enabled = False

    def render(self, context, instance, placeholder):
        context.update({'object': instance})
        return context
