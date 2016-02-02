from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class BlogInfo(models.Model):
    title = models.CharField(max_length = 60)
    description = models.CharField(max_length = 100)

    def __str__(self):
        return "%s %s" % (self.title)

@python_2_unicode_compatible
class User(models.Model):
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    joined_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    pub_date = models.DateTimeField(auto_now_add = True)
    content = models.TextField()

    def __str__(self):
        return self.title
