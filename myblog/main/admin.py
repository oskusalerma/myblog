from django.contrib import admin

from .models import BlogInfo, User, Post

admin.site.register(BlogInfo)
admin.site.register(User)
admin.site.register(Post)
