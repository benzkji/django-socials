from django import forms
from django.utils.translation import ugettext_lazy as _

# from cms.plugin_base import CMSPluginBase

from ..models import Instagram


# class InstagramPluginForm(forms.ModelForm):
#
#     class Meta:
#         model = Instagram
#         fields = '__all__'
#         labels = {}
#         widgets = {}
#
#
# class InstagramPlugin(CMSPluginBase):
#
#     form = InstagramPluginForm
#     model = Instagram
#     module = _('Social')
#     name = _('Instagram')
#     render_template = 'socials/plugins/instagram.html'
#     text_enabled = False
#
#     def render(self, context, instance, placeholder):
#         context.update({'object': instance})
#         return context
