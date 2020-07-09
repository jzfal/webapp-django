from django.shortcuts import render, get_object_or_404
from .models import Post # relative import 
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()  # use a specific query set, if never define queryset, can define model = Post and django will retrieve the generic post object 
    context_object_name = 'posts' # use the context variable posts = queryset instead of the default object list
    paginate_by = 3
    template_name = 'blog/post/list.html'  # use the custom template, if not set, ListView will use the blog/post_list.html

    # as no paginator object is created, we will need to pass page to pagination as page_obj which is created by PostListView
 

def post_list(request):
    """
    the pagination template accepts the posts object as page,
    hence an alias is made, posts as page, hence page.previous_page_number
    in pagination template is the same as posts.previous_page_number
    page hook is done in pagination template, pagination template holds the hook"""
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # specify 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 
                    'blog/post/list.html',
                    {'page': page,
                    'posts': posts})

def post_detail(request, year, month, day, post):
    """
    pass in post object
    """
    post = get_object_or_404(Post, slug=post,
                                status='published',
                                publish__year=year, 
                                publish__month=month,
                                publish__day=day)
    return render(request,
                    'blog/post/detail.html',
                    {'post': post})

