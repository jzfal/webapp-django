from django.shortcuts import render, get_object_or_404
from .models import Post, Comment # relative import
from taggit.models import Tag 
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm


class PostListView(ListView):
    queryset = Post.published.all()  # use a specific query set, if never define queryset, can define model = Post and django will retrieve the generic post object 
    context_object_name = 'posts' # use the context variable posts = queryset instead of the default object list
    paginate_by = 3
    template_name = 'blog/post/list.html'  # use the custom template, if not set, ListView will use the blog/post_list.html

    # as no paginator object is created, we will need to pass page to pagination as page_obj which is created by PostListView
 
def post_share(request, post_id):
    # Retrive post by id
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_url(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                    f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                    f"{cd['name']}\'s comments: {cd['comments']}" 
            send_email(subject, message, 'admin@myblog.com',
                        [cd['to']])
            sent = True # will use this in the template, to display a success message

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
                    {'post':post,
                    'form':form,
                    'sent':sent})


def post_list(request, tag_slug=None):
    """
    the pagination template accepts the posts object as page,
    hence an alias is made, posts as page, hence page.previous_page_number
    in pagination template is the same as posts.previous_page_number
    page hook is done in pagination template, pagination template holds the hook

    tag_slug param is passed in the URL, we then retrieve the Tag object with the given tag
    """
    object_list = Post.published.all()  
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
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
                    'posts': posts,
                    'tag': tag})

def post_detail(request, year, month, day, post):
    """
    pass in post object
    """
    post = get_object_or_404(Post, slug=post,
                                status='published',
                                publish__year=year, 
                                publish__month=month,
                                publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method=='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but dont save to database yet
            new_comment = comment_form.save(commit=False) # creats an instance of the model that the form is linked to and saves it to the database. As commit = False, we create the Comment model instance but dont save this instance to the database yet
            # Assign the current post to the comment, for back ref
            new_comment.post = post
            # Save the comment to DB
            new_comment.save()
    else:
        comment_form = CommentForm()


    # to include the similar posts

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                            .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                            .order_by('-same_tags','-publish')[:4] # exclude those which are draft



    return render(request,
                    'blog/post/detail.html',
                    {'post': post,
                    'comments': comments,
                    'new_comment': new_comment,
                    'comment_form': comment_form,
                    'similar_posts': similar_posts})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title','body'),
            ).filter(search=query)
    return render(request,
                    'blog/post/search.html',
                    {'form': form,
                    'query': query,
                    'results': results})