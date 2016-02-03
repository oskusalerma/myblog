from django.contrib import admin

from .models import BlogInfo, Post

class PostAdmin(admin.ModelAdmin):
    fields = (("author", "title"), ("id", "pub_date"), "content")
    readonly_fields = ("pub_date", "id")

    list_display = ("title", "author", "pub_date", "id")
    list_display_links = ("title",)

admin.site.register(BlogInfo)
admin.site.register(Post, PostAdmin)
