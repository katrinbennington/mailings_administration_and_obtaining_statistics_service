from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "content",
        "preview",
        "created_at",
        "views_counter",
    )
    search_fields = ("name",)
