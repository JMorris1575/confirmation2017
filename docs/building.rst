Building the Confirmation Website
=================================

This document details the process of getting the St. Basil Confirmation Website to work on a local system. This will
be the basis for the final production website to be deployed.

The user App
------------

I decided it would take too long to test the models in ``ModelExperimentation`` so I started building the website to
have something real to work on. I decided to start with logging in and logging out which means I had to create the
``user`` app using ``python manage.py startapp user`` which worked as expected. Let me try a simplified version of
Test Driven Development.

Getting to the Login Page
+++++++++++++++++++++++++

**Does an unauthenticated user get sent to the login page when entering the root url (/)?** No. I need to do some sort
of redirect.

Working Toward a Solution: I read https://docs.djangoproject.com/en/1.11/topics/auth/default/ and, although I'm sure it
contains some very useful information about authentication, it is not what I'm looking for now. I will try to copy what
I did in ModelExperimentation.

Attempt 1: in ``config.urls.py`` add a url pattern as follows::

    ...
    from django.views.generic import RedirectView
    ...
    url(r'^$', RedirectView.as_view(url='login/'),
    ...

Once I got the correct syntax it worked to redirect ``localhost:8000`` to ``localhost:8000/login/``.

This solution, however, does not correspond to what is in *Django Unleashed*. I will look at the authentication video
I downloaded the other night that are in ``Net Gleanings/Video Downloads/Django/jeff n Tutorials`` and found some things
reminiscent of what I read in the documentation above. So, let's try it! It says to put this line into the url patterns
in ``config.urls.py``::

    url('^', include('django.contrib.auth.urls')),

I had to add ``include`` to my ``django.config.urls`` import and create a setting in ``settings.py``::

    LOGIN = '/login/'

Which, he said is not the recommended thing to do but he didn't say what was so I'll leave it for now. (He said
something about using ``reverse_lazy`` but I may have to try that later.)

This did not redirect to /login/ so I added the RedirectView line back in.

**Does the url ``/login/`` result in the display of the login page?** No. I got a "Page not found (404)" error. It
found no reference to ``/login/`` in the url patterns.

Working Toward a Solution: I departed from the strict, or even lenient, TDD path but this is what I had to do::

    * add user.apps.UserConfig to the installed apps
    * add LOGIN_URL = '/login/' to the base.py file
    * use the following as my url patterns:
        urlpatterns = [
            url(r'^$', RedirectView.as_view(url='login/')),
            url(r'^admin/', admin.site.urls),
            url('^', include('django.contrib.auth.urls')),
        ]
    * in the user app folder, create a templates directory containing a registration directory containing login.html
    * created a simple login.html file in the registration directory.

Next I will want to create a ``base.html`` file someplace to form the base of all my html documents.

Improving the Templates
+++++++++++++++++++++++

Based on what is done in *Django Unleashed*, I need to create the main ``base.html`` file in the
``ConfirmationWebsite.templates`` directory and and ``base_<appname>.html`` files in each of the
``<appname>.templates.<appname>`` directories.

Here is ``base.html`` (adapted from *Django Unleashed*)::

    {% load staticfiles %}

    <! DOCTYPE html >

    <html lang="en">

        <head>
            <meta charset="utf-8">
            <title>
                {% block title %}
                    St. Basil Confirmation -
                {% endblock %}
            </title>
            <meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <!--[if IE]><script
                src="http://html5shiv.googlecode.com/svn/trunk/html5.js">
            </script><![endif]-->
            <link rel="stylesheet" type="text/css"
                  href="{% static 'site/normalize.css' %}">
            <link rel="stylesheet" type="text/css"
                  href="{% static 'site/skeleton.css' %}">
            <link rel="stylesheet" type="text/css"
                  href="{% static 'site/custom.css' %}">
            {% block head %}{% endblock %}
        </head>

        <body>
            <div class="container"><!-- container -->
                <header class="row">
                    <div class="offset-by-two eight columns">
                        <h1 class="logo">St. Basil Confirmation Activities</h1>
                    </div>
                </header>
                <div class="status row">
                    <div class="offset-by-eight four columns">
                        <ul class="inline">
                            {% if user.is_authenticated %}
                                <li><a href="{% url 'dj-auth:logout' %}">
                                    Log Out
                                </a></li>
                            {% else %}
                                <li><a href="{% url 'dj-auth:login' %}">
                                    Log In
                                </a></li>
                            {% endif %}
                        </ul>
                    </div>
                </div>
                <main>
                    {% block content %}
                        This is default content!
                    {% endblock %}
                </main>
            </div><!-- container -->

            <footer>
                <p class="offset-by-eight four columns">
                    Modified from base.html created for
                    <a href="https://Django-Unleashed.com/">
                        Django Unleashed</a>
                </p>
            </footer>
        </body>

The ``base_<appname>.html`` files have this form::

    {% extends parent_template|default:"base.html" %}

Now the ``login.html`` file can say::

    {% extends 'user/base_user.html' %}

    {% block title %}Login{% endblock %}

    {% block content %}
        Yay!!!
    {% endblock %}
