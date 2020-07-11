from django.urls import path
from . import views

app_name = 'blog'

# django runs through each URL pattern and stops at the first one that matches the requested URL. Then, Django imports the view of the mathching URL pattern and executes it

urlpatterns = [
    #post views
    path('', views.post_list, name='post_list'), #old url list pattern
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'),
    path('<int:post_id>/share/',
        views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/',
        views.post_list, name='post_list_by_tag'),
]

