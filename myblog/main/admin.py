from django.contrib import admin

from .models import BlogInfo, Post, Comment

class PostAdmin(admin.ModelAdmin):
    fields = (("author", "title"), ("id", "pub_date"), "content")
    readonly_fields = ("pub_date", "id")

    list_display = ("title", "author", "pub_date", "id")
    list_display_links = ("title",)

class CommentAdmin(admin.ModelAdmin):
    fields = ("author", ("id", "pub_date"), "content")
    readonly_fields = ("pub_date", "id")

    list_display = ("author", "post", "pub_date", "id")

admin.site.register(BlogInfo)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
