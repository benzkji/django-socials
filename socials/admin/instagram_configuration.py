from django import forms
from django.contrib import admin
from django.utils import timezone

from ..models import InstagramConfiguration


class InstagramConfigurationAdminForm(forms.ModelForm):

    new_token = forms.CharField(
        required=False,
        help_text='get it from instagram, must be entered only once.',
    )

    def __init__(self, *args, **kwargs):
        super_result = super().__init__(*args, **kwargs)
        show_new = False
        if kwargs.get('initial', None):
            # creation. need a token!
            show_new = True
        elif not self.instance.token_ok:
            # whatever reaseon...a long lived token is again needed.
            show_new = True
        if not show_new:
            self.fields['new_token'].widget = self.fields['new_token'].hidden_widget()
        return super_result

    def save(self, *args, **kwargs):
        if not self.errors:
            if not self.instance.token_ok and self.cleaned_data.get('new_token', None):
                self.instance.token = self.cleaned_data.get('new_token', None)
                # assume it works!
                self.instance.token_refresh_date = timezone.now()
                self.instance.token_ok = True
        return super().save(*args, **kwargs)

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
        'active',
        'posts_refresh_date',
        'token_ok',
        'token_refresh_date',
    ]
    list_filters = ('active', )
    readonly_fields = [
        'date_added',
        'date_changed',
        'token',
        'token_ok',
        'token_refresh_date',
        'posts_refresh_date',
    ]
