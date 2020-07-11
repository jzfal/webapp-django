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

#### The workflow so far 

We first start from the models, we decide what kind of models we will want to have in our application (alot of configuration to be done with regards to querying the objects and persistance in database). We then move on to our overall app settings such that the models are included in the site. Then we move to creating a generic admin login page. After creating the admin page, we move on to creating a form (django alr has a built in form for post, can just use theirs for the time being). We then create view functions (or class) for our custom models, these are all found in the view module of our application. For view functions we need to create url patterns as well as templates to render, using template inheritance and extensions. 


### Enhancing the blog with advanced features

Implement the following features:
- Sharing posts via email
- Adding comments to a post
- Tagging posts
- Recommending similar posts

Cover this following topics:
- Sending emails with Django 
- Creating forms and handling them in views
- Creating forms from models 
- Integrating third-party applications 
- Building complex QuerySets

#### Sharing posts by email
These are the steps:
- Create a form for users to fill in their name, their email, the email recipient, and optional comments
- Create a view in the `views.py` file that handles the posted data and sends the email
- Add a URL patter for the new view in the `urls.py` file of the blog application 
- Create a template to display the form 

#### Creating forms

Django comes with two base classes to build forms:
- Form: Allows you to build standard forms
- ModelForm: Allows you to build forms tied to model instances

All field types from the forms module contain their own field validation. 

#### Handling forms in views

Need to create a new view to handle each form and send an email when its successfully submitted. 

- Define a new view that takes in a request object and the post_id as params
- use `get_object_or_404() to retrieve the post by ID and make sure that the retrieved post has a published status
- You use the same view for both displaying the initial form and processing the submitted data. You differentiate whether the form was submitted or not based on the `request` method and submit the form using `POST`. You assume that if you get a `GET` request, an empty form has to be displayed.
- If form is validated, `form.cleaned_data` is an attribute, a dictionary of form fields and their values. 

#### Sending emails

You need to have a local **Simple Mail Transfer Protocol (SMTP) server**, or you need to define the configuration of an external SMTP server by adding the following settings to the `settings.py` file:
- EMAIL_HOST: The SMTP server host, the default is localhost
- EMAIL_PORT: The SMTP port, the default is 25
- EMAIL_HOST_USER: The username for the SMTP server
- EMAIL_HOST_PASSWORD: The password for the SMTP server
- EMAIL_USE_TLS: Whether to use a Tranport Layer Security (TLS) secure connection 
- EMAIL_USE_SSL: Whether to use an implicit TLS secure connection 

If no SMTP server, can tell DJANGO to write emails to the console by adding the following setting to the `settings.py` file:
`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

By using this setting, Django will output all emails to shell, useful for testing the application without an SMTP server.

Once the view is completed, we need to update the URL pattern for it. Add the post_share URL pattern to `urls.py`.

#### Rendering the forms in templates

After creating the form, view, url, we are left with the template for this view. Create a nwe file in the `blog/templates/blog/post/` directory and name it `share.html`. 

We will need to create the HTML form element in the template, indicating that it has to be submitted by the `POST` method: `<form method="post">`
Then you include the actual form instance. You tell Django to render its fields in HTML paragraph `<p>` elements with the `as_p` method. You can also render the form as an unordered list with `as_ul` or as an HTML table with `as_table`. If you want to render each field, can iterate like this 
```html
{% for field in form %} 
  <div>
      {{ field.errors }}
      {{ field.label_tag }} {{ field }}
  </div>
{% endfor %}
```

The `{% csrf_token %}` template tag introduces a hidden field with an autogenerated token to avoid **cross-site request forgery (CSRF)** attacks.


We also edit the details.html file to include the share post url .
We build the URL dynamically using the `{% url %}` template. We are using the namespace blog and the URL named post_share, and we are passing the post ID as a parameter to build the absolute URL. 

For the form validation, on some browsers, they will display an error message for the fields that are wrong.

#### Creating a comment system
The steps are:
1. Create a model to save comments
2. Create a form to submit comments and validate the input data
3. Add a view that processes the form and saves a new comment to the database
4. Edit the post detail template to display the list of comments and the form to add a new comment

The comment model contains a foreign key to associate a comment with a single post (many to one) relationship. 

The `related_name` attribute allows you to name the attribute that you use for the relationship from the related object back to this one. After defining this, you can retrieve the post of a comment object using `comment.post` and retrieve all comments of a post using `post.comments.all()`. 

The new `Comment` model is not yet sync into the database. Run the command to generate a new migration: `python manage.py makemigrations blog`, this will create the migration script for the comments model 

Now we need to create the related database schema and apply the changes to the database with: `python manage.py migrate`

Now a `blog_comment` table exist in the database

Next we can add the new model to the admin site in order to manage comments through a simple interface. Import the Comment model and add it to the ModelAdmin class.

We need to build a form for the users to comment on blog posts. For the comment form, we need to use `ModelForm` because you have to build a form dynamically from the `Comment` model.

We will use the post detail view to instantiate the form and process it, in order to keep it simple. Edit the `views.py` file, add imports for the Comment model and the CommentForm form, and modify the `post_detail` view 

Now that the comments are functional, we need to adapt the post/detail.html template to do the follwing:

- Display the total number of comments for a post 
- Display the list of comments
- Display a form for users to add a new comment

Use the Django ORM in the template, executing the Queryset comments.count(). Note that the Django template language doesnt use () for calling methods. The `{% with %}` tag allows you to assign a value to a new variable that will be available to be used until the `{% endwith %}` tag.

Also add the pluralize template filte to display a plural suffix for the word "comment".

The admin can deactivate comments from the admin page, comments with active == False will not be diplayed on the post details


#### Adding the tagging functionality

`django-taggit` is a reusable application that primarily offers you a Tag model and a manager to easily add tags to any model. 

First we need to install it by pip.
Then open the settings.py file of mysite and add `taggit` to the `INSTALLED_APPS` setting.

Open the models.py file of the blog app and add the TaggableManager manger provided by django-taggit to the Post model, then update the migrations.

We also need to edit the blog posts to display the tags. 
The join template filter works the same as the Python string join method.

Next edit the post_list view to let users list all posts tagged with a specific tag. Change the `post_list` view to optionally filter posts by a tag. 

After retrieving the tag from the url, we need to filter the list of posts by the ones that contain the given tag. Since this is a many to many relationship, you have to filter posts by tags contained in a given list, which in this case only contains one element. We search with teh `__in` field lookup. Many to many as a post can have multiple tags and a tag can be related to multiple posts. We also need to return the tags that have been found. 

As we modify the path, we have two paths that use the same view. However as both patterns point to the same view, they have different names. Dont forget to change the list html template as we have changed the view function. 

With the if template in out html, a user will see the list of all posts with pagination, if they filter by posts tagged with a specific tag, they will see the tag that they are filtering by. Now we also need to change the way the tags are displayed.

For the new list template, we loop through all the tags of a post displaying a custom link to the URL to filter posts by that tag. We build the URL using the name of teh URL and the slug tag as its parameter. You seperate the tags by commas. Remember that we can pass in arguments to build the url. 


### retrieving posts by similarity

Tags allow you to categorize posts in a non-hierarchical manner. Posts about similar topics will have several tags in common. We will display similar posts by the number of tags they share. 

The steps are:
1. Retrieve all tags for the current post
2. Get all posts that are tagged with any of those tags.
3. Exclude the current post from that list to avoid recommending the same post
4. Order the results by the number of tags shared with the current post
5. In the case of two or more posts with the same number of tags, recommend the most recent post
6. Limit the query to the number posts you want to recommend.

We will add this to the post_detail view. After adding the query and returning it to render.

`django-taggit` alos includes a `similar_objects()` manager that can be used to retrieve objects by shared tags.

#### Summary 

Work with Django forms and model forms. Create a tagging system and recommend similar posts. 