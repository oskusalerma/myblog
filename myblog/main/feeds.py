from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse

from .models import Post, Comment, BlogInfo

def getBI():
    return BlogInfo.objects.all()[0]

class Posts(Feed):
    feed_type = Atom1Feed
    title = getBI().title
    link = "/"
    subtitle = getBI().description

    def items(self):
        return Post.objects.order_by('-pub_date')[:20]

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        return post.content

    def item_pubdate(self, post):
        return post.pub_date

    def item_updateddate(self, post):
        return post.pub_date

    def item_author_name(self, post):
        return post.author.get_username()

    def item_link(self, post):
        return reverse('main:post', kwargs = {"post_id" : post.pk})

class Comments(Feed):
    feed_type = Atom1Feed
    title = getBI().title
    link = "/"
    subtitle = getBI().description

    def items(self):
        return Comment.objects.order_by('-pub_date')[:500]

    def item_title(self, comment):
        return comment.post.title

    def item_description(self, comment):
        return comment.content

    def item_pubdate(self, comment):
        return comment.pub_date

    def item_updateddate(self, comment):
        return comment.pub_date

    def item_author_name(self, comment):
        return comment.author.get_username()

    def item_link(self, comment):
        return "%s#comment_%s" % (
            reverse("main:post", kwargs = {"post_id" : comment.post.pk}),
            comment.pk)
