## Project setup
Run the following command from the command shelll
`django-admin startproject mysite` 

#### directory setup

- `__init__.py` to initialize mysite as a module package
- `asgi.py` This is the configuration to run your project as ASGI, the emergin Python standard for asynchronous web servers and applications
- `settings.py` This indicates settings and configuration for your project and contains initial default settings 
- `urls.py` This is the place where your URL patterns live. Each URL defined here is mapped to a view. 
- `wsgi.py` This is the configuration to run your project as a **Web Service Gateway Interface (WSGI)** application

#### Migration of database models

For the initial configuration, cd to the application dir and run the following:
`python manage.py migrate`

Django will automatically apply the database migrations and create a new sqlite3 db 

#### Running the dev server

Start the dev server with the following command from proj root in this case from `~mysite/`: `python manage.py runserver

### Projects and applications

In Djange, a project is considered a Django installation with some settings. An application is a group of models, views, templates and URL. Applications interact with the framework to provide some specific functionalities and may be reused in various projects. You can think of a project as your website, which contains several applications, such as a blog, wiki, or forum, that can also be used by other projects. 


### Creating first django application

Create a blog application from scratch: `python manage.py startapp blog`

The directory is as follows:
- `admin.py` This is where you register models to include them in the Django administration site-using this site is optional
- `apps.py` This includes the main configuration of the blog application
- `migrations` This directory will contain database migrations of your applications. Migrations allow Django to track your model changes and synchronize the database accordingly.
- `models.py` This includes the data models of your application, all Django applications need to have a models.py file, but this file can be left empty
- `tests.py` This is where you can add tests for your application 
- `views.py` The logic of your application goes here; each view recieves an HTTP request, processes it, and returns a response

#### Models module 

Django comes with different types of field for creation of a relational model, check them out [here](https://docs.djangoproject.com/en/3.0/topics/db/models/#fields)

The Meta class inside the model contains metadata to tell Django to sort results by the publish field in descending order by default when you query the database. You specify the descending order using the negative prefix. By doing this, posts published recently will appear first

- Activating the application
    - In order to keep track of the app and create database tables for the models, we need to activate them. Edit the `settings.py` file and add `blog.apps.BlogConfig` to the `INSTALLED_APPS` settings.

- For db persistance, we use the migrate command to apply migrations for all applications listed in `INSTALLED_APPS`, it sync databases with the current models and existing migrations. 
    - First create an initial migration for the Post model. In the root of the project, run the command: `python manage.py makemigrations blog`
    - There will be a log of migrations kept in the migrations directory of the blog application
    - Taking a look at the SQL code that DJANGO runs to create the table for the model. The `sqlmigrate` command takes the migration names and returns their SQL without executing it. Run the command `python manage.py sqlmigrate blog 0001` to see the SQL output of our first migration 
    - Django creates a primary key automatically for each model, but you can also override this by specifying `primary_key==True` in one of your model fields. The default primary key is an `id` column which consists of an integer that is incremented automatically. 
    - To sync the database with the new model. Run the command `python manage.py migrate` to apply existing migrations, this command will apply migrations for all apps listed in the `INSTALLED_APPS`. 
    - The steps to follow everytime the models.py file is changed is as follows
        1. run `python manage.py makemigrations blog`
        2. run `python manage.py migrate`

#### Create an admin site for models

After defining a Post model, create a simple admin site to manage the blog posts. The `django.contrib.admin` application is already included in the `INSTALLED_APPS` setting, so we do not need to add this. 

- Create a superuser 
    - `python manage.py createsuperuser`
- Go to local host and add relative path to /admin in url
- The Group and User models that you can see are part of the Django authentication framework located in `django.contrib.auth`. All users can be see in the Users tab, including superusers.

#### Add models to the admin site

- Edit the admin.py file of the blog app
- The app will be added to the admin page
- When you register a model in the Django admin site, you get a user-friendly interface generated by introspecting your models that allows you to list, edit, create, and delete objects in a simple way. 

#### Customizing how models are displayed

In order to customize the display, go to `admin.py` in blog application and change the attributes of the model admin class. 


#### Working with QuerySets and managers 

Djangos ORM is compatible with MySQL, PostgreSQL, SQLite, Oracle and MariaDB.
Database of the project can be set in the `DATABASES` setting in the `settings.py` file.
Django can work with multiple databases at a time, and you can program database routers to create custom routing schemes.
The Django ORM is based on QuerySets. A QuerySet is a collection of database queries to retrieve objects from your database. You can apply filters to QuerySets to narrow down the query results based on given parameters. 

- Creating Objects
    - Run `python manage.py shell`
    ```python
    from django.contrib.auth.models import User
    from blog.models import Post
    user = User.objects.get(username='admin')
    post = Post(title='Anoter post',
            slug = 'another-post',
            body = 'Post body',
            author = user)
    post.save()
    ```
    - to show all the posts made by this user
    ```python
    all_posts = Post.objects.all()
    print(all_posts)
    ```

    - can also use the filter method
    ```python
    Post.objects.filter(publish__year=2020) 
    Post.objects.filter(publish__year=2020, author__username='admin')
    Post.objects.filter(publish__year=2020) \ 
                .filter(author__username='admin') # use chaining 
    # or by exclusion
    Post.objects.filter(publish__year=2020) \ 
                .exclude(title__startswith='Why') 
    # or by order by 
    Post.objects.order_by('title') 
    Post.objects.order_by('-title') # desc    
    ```
    - To delete objects
    ```python
    post = Post.objects.get(id=1)
    post.delete() 
    ```
    Deleting objects will also delete any dependent relationship for ForeignKey Objects defined with `on_delete` set to `CASCADE`

    QuerySets are onlu evaluated(translated into SQL to the database) in the following cases:
    - The first time you iterate over them 
    - When you slice them, for instance, `Post.objects.all()[:3]` 
    - When you pickle or cache them 
    - When you call `repr()` or `len()` on them 
    - When you explicitly call `list()` on them  
    - When you test them in a statement, such as `bool()`, `or`, `and`, or `if`


#### Creating custom model managers

Two ways to add or customize managers for your models:
You can add extra manager methods to an existing manager, or create new manager by modifying the initial QuerySet that the manager returns. The first method provides you with a QuerySet API such as `Post.objects.my_manager()`, and the latter provides you with `Post.my_manager.all()`. The manager will allow you to retrieve post using `Post.published.all()`

### Building list and detail views

A Django view is just a Python function that receives a web request and returns a web response. All the logic to return the desired response goes inside the view. 
First, you will create your application views, then you will define a URL pattern for each view, and finally, you will create HTML templates to render the data generated by the views. Each view will render a template, passing variables to it, and will return an HTTP response with the rendered output. 

#### Creating list and detail views

Edit the `views.py` file of blog app
```python 
def post_list(request):
    posts = Post.published.all()
    return render(request, 
                    'blog/post/list.html',
                    {'posts': posts})
```

Request param is required of all views. This function returns a `HttpResponse` object with the rendered text (normally HTML code). Template context processors are just callables that set variables into the context. 

Create another view to display a single post. Add the following function to views.py:
```python 
def post_detail(request, year, month, day, post):
    """
    pass in post object
    """
    post = get_object_or_404(post, slug=post,
                                status='published',
                                publish__year=year, 
                                publish__month=month,
                                publish__day=day)
    return render(request,
                    'blog/post/detail.html',
                    {'post': post})
```
#### Adding URL patterns for your views
URL patterns allow you to map URLs to views. A URL pattern is composed of a string pattern, a view, and, optionally, a name that allows you to name the URL project-wide. Django runs through each URL pattern and stops at the first one that matches the requested URL. Then, Django imports the view of the matching URL pattern and executes it, passing an instance of the `HttpRequest` class and the keyword or positional arguments.

In the `urls.py` file, we define an app namespace with the `app_name` variable. This allows us to organize URLs by app and use the name when referring to them. You define two different patterns using the `path()` function. Use the `<>` to capture values from the url. All path converters can be found on the Django docs.

If using path() and converters is not enough, can use the re_path() and use regex to capture the params.

Next we have to include the URL patterns of the `blog` app to the main URL patterns of the project. 

Edit the `urls.py` file located in the `mysite` dir.


- Canonical URLs for models 
    - A canonical URL is the preferred URL for a resource. You may have different pages in your site where you display posts, but there is a single URL that you use as the main URL for a blog post. The convention in Django is to add a get_absolute_ url() method to the model that returns the canonical URL for the object. We cna use the post_detail URL to build the canonical URL for `Post` objects. For this method, you will use the `reverse()` method, which allows you to build URLs by their name and pass optional parameters. 

#### Creating templates for your views
Templates define how the data is displayed; they are usually written in HTML in combination with the Django template language. 

Create the following directories and files inside your blog application directory:
```templates/
        blog/
            base.html
            post/
                list.html
                detail.html
```

Django has a powerful template language that allows you to specify how data is displayed. It is based on template tags, template variables, and template filters: 
- Template tags control the rendering of the template and look like {% tag %} 
- Template variables get replaced with values when the template is rendered and look like {{ variable }} 
- Template filters allow you to modify variables for display and look like {{ variable|filter }}
Can see more template tags and filters at django docs.

Edit the `base.html` file

`{% load static %}` tells Django to load the static template tags that are provided by the `django.contrib.staticfiles` application, which is contained in the `INSTALLED_APPS` setting. After loading them, you are able to use the {% static %} template tag throughout this template. 

You can see that there are two `{% block %}` tags. These tell Django that you want to define a block in that area. Templates that inherit from this template can fill in the blocks with content. You have defined a block called title and a block called content. 

Edit the `post/list.html` file

With the {% extends %} template tag, you tell Django to inherit from the blog/ base.html template. Then, you fill the title and content blocks of the base template with content. You iterate through the posts and display their title, date, author, and body, including a link in the title to the canonical URL of the post. 
In the body of the post, you apply two template filters: truncatewords truncates the value to the number of words specified, and linebreaks converts the output into HTML line breaks. You can concatenate as many template filters as you wish; each one will be applied to the output generated by the preceding one. 


### Adding pagination

Instead of displaying all the posts on a single page, we split the list with pagination

Edit the `views.py` file of the blog app. After editng the view function to allow for pagination, we need to create a template to display the paginator so that it can be included in any template that uses pagination. In the templates/folder of the blog application, create a new file and name it `pagination.html`.

The pagination template expects a Page object in order to render the previous and next links, and to display the current page and total pages of results. This method can be used in the paginated views of different models, not just for the post model 


### Using class based views

Class based views are an alternative way to implement views as Python objects instead of functions. Since a view is a callable that takes a web request and returns a web response, you can also define your views as class methods. Django provides base view classes for this. All of them inherit from the `View` class, which handles HTTP method dispatching and other common functionalities. 

Class based views have these advantages:
- Organizing code related to HTTP methods, such as GET, POST, or PUT, in separate methods, instead of using conditional branching 
- Using multiple inheritance to create reusable view classes (also known as mixins)

Now change the `post_list` view into a class based view to uses the generic `ListView` offered by Django. This base view allows you to list objecst of any kind.

After changing to a class view, we also need to choose the right page object that is passed to the pagination template. Djangos `ListView` generic view passes the selected page in a variable called `page_obj`, so you have to edit your `post/list.html` template accordingly to include the paginator using the right variable, as follows: `{% include "pagination.html" with page=page_obj %}`

### The workflow so far 

We first start from the models, we decide what kind of models we will want to have in our application (alot of configuration to be done with regards to querying the objects and persistance in database). We then move on to our overall app settings such that the models are included in the site. Then we move to creating a generic admin login page. After creating the admin page, we move on to creating a form (django alr has a built in form for post, can just use theirs for the time being). We then create view functions (or class) for our custom models, these are all found in the view module of our application. For view functions we need to create url patterns as well as templates to render, using template inheritance and extensions. 






