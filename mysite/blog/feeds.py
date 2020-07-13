from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):

    """the title, link, and description attributes correspond to the <title>, <link> and <description> RSS elements respectively.

    You use the reverse_lazy() to generate the URL for the link attribute. The reverse() method allows you to build URLs by their name and pass optional parameters. This is a lazily evaluated version of reverse(). It allows you to use a URL reversal before the projects URL configuration is loaded
    
    """ 
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        """ for all objects """
        return Post.published.all()[:5]

    def item_title(self, item):
        """for each object"""
        return item.title

    def item_description(self, item):
        """for each object"""
        return truncatewords(item.body, 30)

