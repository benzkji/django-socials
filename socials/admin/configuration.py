from django import forms
from django.contrib import admin

from ..models import Configuration


class ConfigurationAdminForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Configuration
        labels = {}
        widgets = {
            'url': forms.TextInput
        }


class ConfigurationAdmin(admin.ModelAdmin):

    form = ConfigurationAdminForm
    list_display = [
        'name',
    ]
    readonly_fields = [
        'date_added',
        'date_changed',
        'date_changed',
    ]
