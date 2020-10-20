from django import forms
from django.contrib import admin

from ..models import Post


class PostAdminForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Post
        labels = {}
        widgets = {}


class PostAdmin(admin.ModelAdmin):

    form = PostAdminForm
    list_display = [
        'get_admin_thumbnail',
        'date',
        'get_title',
        'published',
        'configuration',
    ]
    list_filter = [
        'published',
        'configuration',
    ]
    readonly_fields = [
        'get_admin_thumbnail',
        'date',
        'configuration',
        'original_id',
        'data',
    ]
