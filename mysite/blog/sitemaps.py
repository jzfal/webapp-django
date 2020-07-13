from django.contrib.sitemaps import Sitemap
from .models import Post 

class PostSitemap(Sitemap):
    """
    Both the changefreq and priority attributes can be either methods or attributes. 
    """
    
    changefreq = 'weekly'
    priority = 0.9 # max value is 1

    def items(self):
        """
        returns the query set of objects to include in this sitemap
        
        by default Django calls teh `get_absolute_url()` method on each object to retrieve its URl. If you want to specify the URL for each object, you can add a `location` method to your sitemap class
        """
        return Post.published.all()

    def lastmod(self, obj):
        """
        this recieves each object returned by items() and returns the last time the object was modified
        """
        return obj.updated # return the attrib updated

    # def location(self):
    #     # if we want to specify the url to return
    #     pass

