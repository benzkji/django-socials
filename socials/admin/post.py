from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    list_links = [
        "get_admin_thumbnail",
        "date",
    ]
    list_display = [
        "date",
        "get_admin_thumbnail",
        "get_admin_title",
        "published",
        "configuration",
    ]
    list_editable = [
        "published",
    ]
    list_filter = [
        "published",
        "configuration",
    ]
    readonly_fields = [
        "get_admin_thumbnail",
        "date",
        "configuration",
        "original_id",
        "original_data",
    ]
