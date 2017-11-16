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

Working Toward a Solution: I departed from the strict, or even lenient, TDD path but this is what I had to do:

* add user.apps.UserConfig to the installed apps
* add LOGIN_URL = '/login/' to the base.py file
* use the url patterns: [url(r'^$', RedirectView.as_view(url='login/')), url(r'^admin/', admin.site.urls), url('^', include('django.contrib.auth.urls')),]
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

Logging In
++++++++++

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. Django throws
some goofy ProgrammingError about ``"auth_user" does not exist``. I need to run ``python manage.py createsuperuser``.

**Can you create a superuser?** No. It threw the same error as before but, in the command window, Django also reminded
me to perform a ``python manage.py migrate``. When I did that it did mention that "auth" was one of the migrations it
performed.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. It just keeps
returning to the login page with no error messages. I will have to deal with that (the no error messages) later.
Otherwise I need to create some users after creating a superuser.

**Can you create a superuser?** Yes. I used 'Jim' as my username, 'FrJamesMorris@gmail.com' as my e-mail and
dylan-selfie as my password.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. It seems to be
accepting the username and password I created for the superuser but tries to send me to the default
``/accounts/profile/`` page. I need to add a welcome page and the means of arriving there.

Arriving at the Welcome Page
++++++++++++++++++++++++++++

What I think I need to do is:

#. Import reverse_lazy from django.core.urlresolvers
#. Add a LOGIN_REDIRECT_URL to base.py
#. Create a new 'activities' app that will hold the welcome page
#. Include the activities url patterns in config.urls.py
#. Create an activities_welcome.html page to display the welcome page
#. Create a view to control what gets rendered on that page

I learned that number 1 was already done, but not used yet.

For number 2 I added LOGIN_REDIRECT_URL = reverse_lazy('welcome')

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. It says:
``Reverse for 'welcome' not found. 'welcome' is not a valid view function or pattern name``. I'll make it a valid
pattern name as in step 4 above.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. The name
'activities' was not defined because I have neither created it nor imported it into base.py. I will import it into
``config.urls.py`` even though it doesn't yet exist.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. I got a
``module not found`` error. I will use ``python manage.py startapp activities`` to create the activities app.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. ``startapp``
does not create a default ``urls.py`` file. I will create it myself.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. Importing
``activities.urls`` into ``config.urls`` does not seem to work. I will change the url pattern to
``url('^activity/', include('activity.urls'), name='welcome')``

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. But I'm getting
closer. It got to ``activity/urls`` (I changed the name of the ``activities`` app above to ``activity``) but found an
empty file. I will put the following into it::

    from django.conf.urls import url

    urlpatterns = [
        url(r'^$', WelcomePage.as_view(), name='welcome_page')
    ]

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. ``WelcomePage``
is not defined in ``activity.urls.py`` I will import it.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. It cannot import
``WelcomePage`` because that view does not exist. I will create it as a stub.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. This time it
says ``'WelcomePage' has no attribute 'as_view'`` I think I need to subclass Views in my WelcomePage class. Before that
I need to import it from django.views.generic.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. But it went back
to telling me ``Reverse for 'welcome' not found. 'welcome' is not a valid view function or pattern name.`` It is a valid
pattern name now so it must be looking for the view to return something. I added a simple function to it::

    class WelcomePage(View):

        def get(self, request):
            return(request)

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. It kept telling
me ``'welcome' is not a valid view function of pattern name.`` It needed a ``post`` method in the WelcomePage class::

    class WelcomePage(View):

        def get(self, request):
            return render(request)

        def post(self, request):
            return render(request)

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. ``render()``
has ``1 required positional argument: 'template_name'``. I will add one: ``template_name = 'actiity/welcome.html'``

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. But now I got
``TemplateDoesNotExist at /activity/welcome/``. I will add a stub welcome.html file to ``activity.templates.activity``.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. Still can't find
the template maybe ``template_name = 'welcome/welcome.html'`` will work.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. It kept giving
me the ``TemplateDoesNotExist`` error. I finally realized I haven't informed Django that the activity app exists. I will
add ``'activity.apps.ActivityConfig',`` to the ``INSTALLED_APPS`` variabe in ``base.py``.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. A message in
the terminal says
``ModuleNotFoundError: No module named 'activity.apps.ActivityConfig'; 'activity.apps' is not a package``. Inside the
``apps.py`` file the class name was still ``ActivitiesConfig`` so I changed it to ``ActivityConfig``.

**Does entering a username and password on the login page result on arriving at the Welcome page?** No. It got to a
page with the proper header and footer but it still contained the default content. I will add the {% block content %}
and {% endblock %} around the 'Got to the Welcome page!' stub.

**Does entering a username and password on the login page result on arriving at the Welcome page?** Yes! Hurray! Now I
can do something else.

Addingg the Activity List to the Welcome Page
+++++++++++++++++++++++++++++++++++++++++++++

This will Finishing the welcome page is going to require me to:

#. Update ``welcome.html`` to include the display of a list of activities
#. Update the ``get`` method in the WelcomePage view class to feed the template the right values
#. Create the Activity model, make migrations and migrate
#. Make it look nice with css

I thought of a better way to document my approach to Test Driven Development. Each question can appear as the title of
a csv-table with the results and subsequent actions as the table columns.

.. csv-table:: **Does a list of activities appear on the welcome page?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, Add a simple listing to the ``welcome.html`` file using the context variable ``activities``
    No, page displayed with no list; update the ``get`` method in WelcomePage view
    No, ImportError upon writing :ref:`import<act_import>`; create the :ref:`model<activity_model>` and migrate.
    No, still nothing in list; :ref:`send a context variable<send_context>` from ``views.WelcomePage.get``.
    No, use admin app to add some activities
    No, register Activity in ``activities.admin.py``: ``from .models import Activity... admin.site.register(Activity)``
    No, nothing to show in list; add four activities to the Activity model
    Yes!, Now to make it look nice

.. _act_import:

The Activity model import in ``activity.views.py``::

    from .models import Activity

.. _activity_model:

The Activity Model::

    class Activity(models.Model):
        number = models.IntegerField(unique=True)
        name = models.CharField(max_length=100)
        slug = models.SlugField()

        def __str__(self):
            return self.name

.. _send_context:

Sending the 'activities' context variable from activity.views.WelcomePage.get::

        def get(self, request):
            activities = Activity.objects.all()
            return render(request, self.template_name, {'activities': activities})






Things I Learned or Still Need to Study
---------------------------------------

Static Files
++++++++++++

In order to get the ``skeleton.css`` files etc. to work I had to put these lines into my ``base.py`` program::

    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static", "site" ), )

and the references to them had to change to::

        <link rel="stylesheet" type="text/css"
              href="{% static '/normalize.css' %}">
        <link rel="stylesheet" type="text/css"
              href="{% static '/skeleton.css' %}">
        <link rel="stylesheet" type="text/css"
              href="{% static 'custom.css' %}">

I'm not sure why I couldn't do it as it was done in *Django Unleashed* but whatever works is fine by me.

**I may need to study how Django handles static files.**

