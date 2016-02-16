from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class BlogInfo(models.Model):
    title = models.CharField(max_length = 60)
    description = models.CharField(max_length = 100)

    def __str__(self):
        return "%s" % (self.title)

@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    pub_date = models.DateTimeField(auto_now_add = True, db_index = True)
    content = models.TextField()

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add = True)
    content = models.TextField()

    def __str__(self):
        return "%s - %s" % (self.author.get_username(), self.pub_date)
