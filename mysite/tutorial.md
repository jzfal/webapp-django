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


### Extending the blog application


Will cover:
- Creating custom tempate tags and filters
- Adding a sitemap and post feed
- Implementing full-text search with PostgreSQL

#### Custom template tags
Django provides the following helper functions
- simple_tag: Processes the data and returns a string
- inclusion_tag: Processes the data and returns a rendered template

Template tags must live inside the Django applications

The file structure of the blog application should look like this

```
blog/
    __init__.py
    models.py
    ...
    templatetags/
        __init__.py
        blog_tags.py
```

Each module that contains template tags needs to define a variable called `register` to be a valid tag library. This variable is an instance of `template.Library`, and its used to register your own template tags and filters

Before using custom template tags, you have to make them available for the template using the `{% load %}` tag. We need to use the name of the Python module containing your template tags and filters.

The power of custom template tags is that you can process any data and add it to any template regardless of the view executed. You can perform QuerySets or process any data to display results in your templates (server side rendering)

Will also create an inclusion tag. We can render a template with context variables returned by your template tag. 

The inclusion tag returns a dictionary of variables instead of a simple value, as compared to the prev tag. This is used as context to render the specified template. The template tag allows to specify the optional number of posts to display.

We use the inclusion template within the base template, by calling the function. 


Finally, create simple tag that returns a value. Will store the result in a varible that can be reused, rather than directly outputting it. You will create a tag to display the most commented posts. Can call the varible globally using ` {% get_most_commented_posts as most_commented_posts %}`

#### Custom template filters

You can use the capfirst filter to capitalize the first character of the value, like {{ value|capfirst }}, to return a value. You can apply as many filters as you like to a variable, for example,  `{{ variable|filter1|filter2 }}`

Create a custom filter to enable you to use markdown syntax in your blog posts and then convert the post contents to HTML in the templates. First install Python `markdown` module via pip: `pip install markdown==3.2.1`
Edit the blog.py file. 

Django escapes the HTML code generated by filters, characters of HTML entities are replaced with their HTML encoded charaters, to prevent outputting of dangerous HTML.

Next load the template tags module in the post list and detail templates. Add the following line to list.html and detail.html after the {% extends %} tags: `{% load blog_tags %}`

The `truncatewords_html` filter truncates a string after a certain number of words, avoiding unclosed HTML tags.

Now open ` http://127.0.0.1:8000/admin/blog/post/add/ ` in your browser and add a post with the following body:
```markdown

This is a post formatted with markdown -------------------------------------

*This is emphasized* and **this is more emphasized**.

Here is a list:

* One 
* Two 
* Three

And a [link to the Django website](https://www.djangoproject.com/) 
```

#### Adding a sitemap to your site

Django comes with a sitemap framework, allows to generate sitemaps for the site dynamically. A sitemap is an XML file tha tells search engines the pages of your website, their relevance, and how frequently they are updated. Using a sitemap will make your website more visible in search engine rankings: sitemaps help crawlers to index your websites content

The Django sitemap framework depends on django.contrib.sites, which allows you to associate objects to particular websites that are running with your project. This comes in handy when you want to run multiple sites using a single Django project. To install the sitemap framework, you will need to activate both the `sites` and the `sitemap` applications in your project. 

Edit the `settings.py` file of your project and add django.contrib.sites and django.contrib.sitemaps to the `INSTALLED_APPS` setting. Also, define a new setting for the site ID, as follows:

```python

SITE_ID = 1
# application definition
INSTALLED_APPS = [
    # ...
    'django.contrib.sites',
    'django.contrib.sitemaps',
]
```

Now run the following command to create tables of the Django site application in the database: `python manage.py migrate`

The sites application is now synced with the database.

Next create a new file inside the blog application and name it `sitemaps.py` (will tell django the config of the objects to our sitemaps)

Finally we need to add the sitemap URL. Edit the main `urls.py` file of the project and add the sitemap. 

We include the required imports and define a dict of sitemaps. The defined URL pattern matches `sitemap.xml` and uses the sitemap view. The sitemaps dictionary is passed to the sitemap view. 

Now run the dev server and open ` http://127.0.0.1:8000/sitemap. xml`. The url for each post has been built using the get_absolute_url() method.The lastmod attribute corresponds to the post `updated` date field.

You can see that the domain used to build the URLs is example.com. This domain comes from a Site object stored in the database. This default object was created when you synced the site's framework with your database. 

Open `http://127.0.0.1:8000/admin/sites/site/` in your browser. As admin, we can see the list diplay for the sites framework. Here we can set the domain or host to be used by the sites framework and the applications that depend on it. In order to generate URLs that exist in your local env, change the domain name to `localhost:8000`, and save it. The URLs displayed in your feed will now be build using this hostname, in a production env, you will have to use your own domain name for the sites framework.


#### Creating feeds for your blog posts

Django has a built-in syndication feed framework that you can use to dynamically generate RSS or Atom feeds in a similar manner to creating sitemaps using the site's framework. A web feed is a data format (usually XML) that provides users with the most recently updated content. Users will be able to subscribe to your feed using a feed aggregator (software that is used to read feeds and get new content notifications). 

Create a new file in the blog app and name it `feeds.py`. 
Now edit the blog/urls.py and import the LatestPostsFeed class we created, and instantiate the feed in a new URL pattern. Navigate to  `http://127.0.0.1:8000/blog/feed/` to see the RSS feed. If you open the same URL in an RSS client, we will be able to see the feed with a user friendly interface. 

The final step is to add a feed subscription link to the blogs sidebar. Open the blog/base.html template and modify the sidebar div to include the RSS feed link

#### Adding full text search to the blog

Next, you will add search capabilities to your blog. Searching for data in the database with user input is a common task for web applications. The Django ORM allows you to perform simple matching operations using, for example, the contains filter (or its case-insensitive version, icontains). You can use the following query to find posts that contain the word framework in their body:

```python

from blog.models import Post 
# or alternative can load all and use regex
Post.objects.filter(body__contains='framework')
```

However, if you want to perform complex search lookups, retrieving results by similarity, or by weighting terms based on how frequently they appear in the text or by how important different fields are (for example, relevancy of the term appearing in the title versus in the body), you will need to use a full-text search engine. When you consider large blocks of text, building queries with operations on a string of characters is not enough. Full-text search examines the actual words against stored content as it tries to match search criteria. 

Django provides a powerful search functionality built on top of PostgreSQL's full-text search features. The `django.contrib.postgres` module provides functionalities offered by PostgreSQL that are not shared by the other databases that Django supports. 

We are currently using SQLite for the blog project which is sufficient for a dev env, however, for a prod env, we need a more powerful database, such as PostgreSQL.

If using Linux, install with the command: `sudo apt-get install postgresql postgresql-contrib`

If using macOS or windows, download PostgreSQL from `https://www.postgresql.org/download/` and install it.

You also need to install the psycopg2 PostgreSQL adapter for Python. Run the following command: `pip install psycopg2-binary==2.8.4`


Create a user for the PostgreSQL database. Run the following commands: 
```shell
# su - postgres
# createuser -dP blog

# may be incorrect try
psql -U postgres
# then type in the user password
createdb -E utf8 -U blog blog
```
As user postgres has already been created, to access the user run command `psql postgres`, then type in the password when prompted. To create a new database, go to the pgadmin browser and create new db.

Then edit the settings.py and modify the DATABASES setting , change the default params.After editing, run the migration command: `python manage.py migrate`
Finally create a superuser with the following command:
`python manage.py createsuperuser`

For simple search lookups, edit the settings.py file and add django.contrib.postgres to the INSTALLED_APPS setting, as follows:
```python
INSTALLED_APPS = [
    # ...
    'django.contrib.postgres',
]
```

Now we can search against a single field using the search QuerySet lookup, like this:
```python
from blog.models import Post
Post.objects.filter(body__search='django')
```

This query uses PostgreSQL to create a search vector for the body field and a search query from the term django. Results are obtained by mathcing the query with the vector.

For search against multiple fields. You will need to define a `SearchVector` object. Build a vector that allows you to search against the title and body fields of the Post model.

```python
from django.contrib.postgres.search import SearchVector
from blog.models import Post

Post.objects.annotate(
    search=SearchVector('title', 'body'),
).filter(search='django')
```

*hint: full text search is an intensive process. If you are searching for more than a few hundred rows, you should define a functional index that matches the search vector you are using. Django provides a SearchVectorField field for your models*

#### Building a search view
Create custom view for users to search posts. Create search form. Edit the forms.py. Then edit the views.py. In the view, to check whether a form is submitted, you look for the query param in the request.GET dict. You send the form using the GET method instead of POST, so that the resulting URL includes the query param and is easy to share.

We need to create a template to display the form and the results when the user performs a search. Create search.html in post template directory.

And finally we edit the urls.py to add the pattern for the search view. And finally the basic search engine is created

#### Other full-text search engines
You may want to use a full-text search engine other than from PostgreSQL. If you want to use Solr or Elasticsearch, you can integrate them into your Django project using Haystack. Haystack is a Django application that works as an abstraction layer for multiple search engines. It offers a simple search API that is very similar to Django QuerySets. 

#### summary 
- Creating custom django template tags and filters
- Created sitemap for search engines to crawl the site and and RSS feed for users to subscribe to the blog. 
- Built a search engine using the full text search engine of PostgreSQL

