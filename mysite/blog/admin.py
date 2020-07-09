from django.contrib import admin
from .models import Post  # .models state it as relative path, in curr dir
# Register your models here.
import random

# admin.site.register(Post) # register model --> generate UI to list, edit, create and delete objects 


@admin.register(Post) # Post model is registered in the site using a custom class that inherits from ModelAdmin.
class PostAdmin(admin.ModelAdmin):
    # includes information about how to display the model in the site and how to interact with it. 
    list_display = ('title', 'slug', 'author', 'publish', 'status')  # this attribute allows you to set the fields of your model that you want to display on the admin object list page
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}  # prepopulate this from 'title'
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status','publish')

  