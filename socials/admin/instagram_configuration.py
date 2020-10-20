from django import forms
from django.contrib import admin

from ..models import InstagramConfiguration


class InstagramConfigurationAdminForm(forms.ModelForm):

    short_lived_token = forms.CharField(
        required=False,
        help_text='get it from instagram, must be entered only once.',
    )

    def __init__(self, *args, **kwargs):
        super_result = super().__init__(*args, **kwargs)
        short = False
        if kwargs.get('initial', None):
            # creation. no doubt we need the short lived token.
            short = True
        elif not self.instance.token_ok:
            # whatever reaseon...re-get a long lived token is needed.
            short = True
        if not short:
            self.fields['short_lived_token'].widget = self.fields['short_lived_token'].hidden_widget()

    class Meta:
        fields = '__all__'
        model = InstagramConfiguration
        labels = {}
        widgets = {
            'url': forms.TextInput
        }


class InstagramConfigurationAdmin(admin.ModelAdmin):

    form = InstagramConfigurationAdminForm
    list_display = [
        'name',
    ]
    readonly_fields = [
        'date_added',
        'date_changed',
        'token',
        'token_ok',
        'token_refresh_date',
    ]
