from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse

from .models import Post, BlogInfo

def getBI():
    return BlogInfo.objects.all()[0]

class Posts(Feed):
    feed_type = Atom1Feed
    title = getBI().title
    link = "/"
    subtitle = getBI().description

    def items(self):
        return Post.objects.order_by('-pub_date')[:10]

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        return post.content

    def item_pubdate(self, post):
        return post.pub_date

    def item_updateddate(self, post):
        return post.pub_date

    def item_link(self, post):
        return reverse('main:post', kwargs = {"post_id" : post.pk})
