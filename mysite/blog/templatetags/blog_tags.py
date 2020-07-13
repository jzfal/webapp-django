from django import template
from django.db.models import Count
from ..models import Post
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    """
    djang will use the decorator to register the function as a simple tag. Django will use the functions name as the tag name, if you want to register it using a different name, you can do so by specifying a name attribute, such as @register.simple_tag(name='my_tag') 
    """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    register the template and specify the template that will be rendered with the returned values using `blog/post/latest_post/latest_posts.html

    allows us to render this template within the base template
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    # to prevent nameclash name the function markdown_format but name the filter markdown in the decorator
    return mark_safe(markdown.markdown(text))