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

The Welcome Page
----------------

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

Adding the Activity List to the Welcome Page
++++++++++++++++++++++++++++++++++++++++++++

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

Making the Welcome Page Look Better
+++++++++++++++++++++++++++++++++++

Here I just played with the ``welcome.html`` and ``custom.css`` files until I was happy with what I have so far. I will
have to change it later when I have more information available, such as the number of pages in each activity (which I
may call 'events' or 'tasks' [ugh!] or 'parts' or something) to indicate how much there is to an activity. Other
information can be displayed, such as how far the user is along in each activity, which ones are completed (indicate by
color?) etc.

Here is the for loop in the ``welcome.html`` file::

        {% for activity in activities %}
            <ul class="activity-list">
                <li class="row">
                    <div class="offset-by-one four columns">
                        {{ activity.number }}. {{ activity }}
                    </div>
                </li>
            </ul>
        {% endfor %}

Here is the new ``.activity-list`` selector in the ``custom.css`` file::

    .activity-list {
        list-style-type: none;
        color: #2eb873;
        font-weight: bold;
        margin-top: 20px;
    }

Displaying the Activity Pages
-----------------------------

Linking to the Activities
+++++++++++++++++++++++++

The list items on the Welcome page are supposed to be links to the actual activity pages. To implement this I think I
will need to:

#. Make the activity list items into links to the first page of the corresponding activity.
#. Create the ``activity.urls`` pattern to pick up the slug for page 1.
#. Create a view in ``activity.views`` to render the page
#. Create the Page model in ``activity.models``
#. Create a template ``instruction_page.html`` for the view to render

.. csv-table:: **Does clicking on an activity bring me to the instruction page for that activity?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, Nothing at all happens. Convert the list items to links
    No, 'Page not found'; create a :ref:`url pattern<page-url>` in ``activity.urls`` and corresponding stub view
    No, still couldn't fine it; error in url pattern; try a :ref:`new one<new-page-url>`.
    No, it got to the url but there was nothing to get; fill out the :ref:`PageDisplay`<page-display-01>` view.
    No, get() got an unexpected keyword argument 'slug'; include ``slug`` ``and page_number`` in the call to ``get()``
    No, TemplateDoesNotExist; create ``page_display.html`` in ``activity.templates.activity``
    No, the view does not use page data; modify :ref:`PageDisplay<page-display-02>` to use the (non-existent) Page model
    No, no Page model; create a :ref:`Page model<page-model>`; add to ``admin.py``; update the :ref:`template<page-display-03>`.
    Yes, Now I can add some questions (try to dump the database for transfer to other computers).


.. _page-url:

Here is the new url::

     url(r'^(?P<slug>[\w\-]+)/(?P<page_number>)/$', PageDisplay.as_view(), name="page_display"),

.. _new-page-url:

That one didn't work. I neglected to indicate a pattern for the <page_number>. Here is a better one::

     url(r'^(?P<slug>[\w\-]+)/(?P<page_number>[0-9]+)/$', PageDisplay.as_view(), name="page_display"),

.. _page-display-01:

Here is the first try at the PageDisplay view::

    class PageDisplay(View):
        template_name = 'activity/page_display.html'

        def get(self, request):
            return render(request, self.template_name)

.. _page-display-02:

Here is the second form of the PageDisplay view::

    class PageDisplay(View):
        template_name = 'activity/page_display.html'

        def get(self, request, slug=None, page_number=None):
            pages = Page.objects.filter(activity__slug=slug)
            return render(request, self.template_name, {'pages':pages})

.. _page-model:

Here is the current form of the page model. I should be able to make a combination of activity and number unique
though. (I can! Using the Meta class as shown below and order the listings as well.)::

    class Page(models.Model):
        activity = models.ForeignKey(Activity)
        number = models.IntegerField()
        type = models.CharField(max_length=15,
                                choices=[('IN', 'Instructions'),
                                         ('MC', 'Multichoice'),
                                         ('ES', 'Essay'),
                                         ('AN', 'Anonymous')])
        timed = models.BooleanField(default=False)

        def __str__(self):
            return str(self.activity) + " Page: " + str(self.number)

    class Meta:
        unique_together = ('activity', 'number')
        ordering = ['activity', 'number']

.. _page-display-03:

Here is the version of page-display.html that lists all the available pages for an activity::

    {% extends 'activity/base_activity.html' %}

    {% block content %}
        <ul>
            {% for page in pages %}
                <li>{{ page }}</li>
            {% endfor %}
        </ul>
    {% endblock %}

At this point I had to move everything to the :ref:`rectory computer<moving_to_rectory>`.

Improving the looks of page-display.html
++++++++++++++++++++++++++++++++++++++++

I noticed that the list of pages one gets after clicking on the activity name looks different than the list of
activities even though they are under the same css class in custom.css. I suspect this is because one set, the
activity set, is coded as links (the '<a>' tag), while the other is just a set of list items. If so, this will be
fixed when I create links to the actual question pages.

By the way, it seems the page they get to when clicking on an activity is more like a table of contents page. Perhaps I
should call it that. ... After further thought, it is only a table of contents page for such things as the Abraham
Saga that comes in several episodes, each with its own set of questions. I decided to add ('CO', 'Table of Contents')
to the list of choices for the type of page in the Page model.

Side Task: Getting a Welcome and Logout link into the Header
------------------------------------------------------------

Hopefully this will be a simple task mostly taken care of in the ``base.html`` template using the framework given me by
skeleton.css. Here we go:

.. _welcome_message_table:

Welcome Message
+++++++++++++++

.. csv-table:: **Does 'Welcome' and the user's first name appear on the right hand bottom part of the header?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, It is not in the template; :ref:`add it now<welcome_msg>`.
    No, It appears to the left and even on the login page. Change class to u-pull-right; add {% if user.authenticated %}
    No, It doesn't appear on the login page OR after logging in! Change to {% if user.is_authenticated %}
    No, I hadn't entered my first name into the database. Add my first name.
    Yes, :ref:`'Welcome Jim'<table_error>` appears in the same font as the heading at the right side of the header.

Logout Link
+++++++++++

.. csv-table:: **Does a link to Logout appear to the right of the "Welcome <user_first_name>" message?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, I haven't put that into the ``base.html`` file yet. Change :ref:`base.html<logout_link>`.
    Yes, but the styling needs help.

.. _welcome_msg:

Here is my first attempt::

    <header class="row">
        <div class="two columns">
            <img class="u-max-full-width" src="{% static 'images/HolyspiritYellowRedFlipped.png' %}">
        </div>
        <div class="ten columns">
            <h2 class="logo">St. Basil Confirmation Activities</h2>
        </div>
        <div class="pull-right">
            <h4>Welcome {{ user.first_name }}</h4>
        </div>
    </header>

.. _logout_link:

This worked right away::

    <div class="u-pull-right">
        {% if user.is_authenticated %}
            <a href="logout/">Logout</a>
        {% endif %}
    </div>
    <div class="u-pull-right">
        {% if user.is_authenticated %}
            <h4>Welcome {{ user.first_name }}</h4>
        {% endif %}
    </div>

The formatting needs help however. The Logout link is too close to the welcome message and is lined up with the upper
part of the welcome message and is the wrong color. I can probably fix that all with css.

Making the Header Look Nice
+++++++++++++++++++++++++++

First I created a custom.css class called 'welcome' that sets the font to Arial, the color to the golden yellow color:
#ffdd55.  I also set the font-weight to bold and the margin-right to 20px.

Similarly I created a 'link' class with Arial font, color #ffdd55 and margin-right to 20px.

That looks good enough for now.

Making the Logo into a Link to the Welcome Page
+++++++++++++++++++++++++++++++++++++++++++++++

One way to do this is to wrap it in an <a> tag with href="activity/welcome/". Let's see if this works...

No, it didn't. It sent me to the current url with the 'activity/welcome/' url tacked on to the end of it:
``activity/welcome/activity/welcome/`` for instance. I looked in my urls in the config directory and the activities app
and decided to use ``<a href="{% url 'welcome_page' %}">... </a>`` and that worked as I wanted.

Fixing the URL Patterns
+++++++++++++++++++++++

I noticed, when studying the urls above, that the urls.py file in config have an entry
``url('^activity/', include('activity.urls'), name='welcome'),`` which I need, but I don't think it needs a name. I will
remove the name and see if it makes any difference. (It doesn't seem to.)

Getting Login and Logout Working Properly
-----------------------------------------

The Logout link should log a person out of the website and return automatically to the login page. What I did in
Christmas2017, based on *Django Unleashed* chapter 19, looks complicated. Here goes a Test Driven Development/Learning
process to try to figure it out. (Note: this was started before I made the logo into a link and fixed the naming of one
of the url patterns in the two sections immediately preceding this one.)

.. csv-table:: **Does clicking the Logout link log the user out and return to the Login Page?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, it throws a page not found error for ``<current url>/logout/``; set ``LOGOUT_URL`` in base.py to ``'/logout/'``
    No, no change; name urls from django.contrib.auth.urls to auth_urls and change LOGOUT_URL to reverse that
    No, no change; create urls in user app as per *Django Unleashed* 19.5.2; test login first

.. csv-table:: **Does a user see the login page when entering the website?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, it tries to go to ``login/`` not ``user/login``; set ``LOGIN_URL = reverse_lazy('login')`` in base.py
    No, no change; point RedirectView in config.urls.py to ``pattern_name=login``
    Yes, but I fear unauthenticated users can get in by typing ``activity/welcome`` -- they can! Fix later.

Back to the original problem:

.. csv-table:: **Does clicking the Logout link log the user out and return to the Login Page?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, ``/logout/`` after current url; add 'logout' :ref:`pattern<logout_url>`; set LOGOUT_URL=reverse_lazy('logout')
    No, same problem; change to ``<a href="{% url 'logout' %}>`` in base.html
    No, got to Django logout page; base logout url pattern on *Django Unleashed* :ref:`Example 19.37<ex_19.37>`
    Yes, but any user knowing the url patterns can get in without being logged in

.. _logout_url:

Here is the url pattern I put in ``userl/urls.py``::

    ``url(r'^logout/$', auth_views.logout, name='logout')``

.. _ex_19.37:

Here is my version of the logout url pattern::

    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/login.html',
         'extra_context': {'form': AuthenticationForm}},
        name='logout'),

I noticed that *Django Unleashed* Example 19.45 set ``LOGIN_URL = reverse_lazy('dj-auth:login')`` and
``LOGOUT_URL = reverse_lazy('dj-auth:logout')``. Considering that they didn't seem to have any effect on what I did
above, I changed them for whatever benefit they will have later.

But the authentication still isn't really working. Once I've logged out I can't seem to log back in! It keeps sending
me to ``user/logout/``. More study is necessary. Start on page 468 of *Django Unleashed*, then make the ``dj-auth``
changes above.

I've done all that and here are the current forms of the affected files:

**config\urls.py**::

    from django.conf.urls import include, url
    from django.contrib import admin
    from django.views.generic import RedirectView

    urlpatterns = [
        url(r'^$', RedirectView.as_view(pattern_name='dj-auth:login', permanent=False)),
        url(r'^admin/', admin.site.urls),
        url('^activity/', include('activity.urls')),
        url('^user/', include('user.urls', app_name='user', namespace='dj-auth')),
    ]

**user\urls.py**::

    from django.conf.urls import url
    from django.contrib.auth import views as auth_views
    from django.contrib.auth.forms import AuthenticationForm
    from django.views.generic import RedirectView

    urlpatterns = [
        url(r'^k$', RedirectView.as_view(pattern_name='login', permanent=False)),
        url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
        url(r'^logout/$', auth_views.logout, {'template_name': 'registration/login.html',
                                              'extra_context': {'form': AuthenticationForm}}, name='logout'),
    ]

The reference to ``logout`` in ``base.html`` also had to be changed to ``dj-auth:logout``

But logout still isn't really working. I think I need to set the link to user/login, that is, ``dj-auth:login`` to get
it to automatically go back to the login page after logging out. But then would I really be logged out? I will try an
experiment using the Welcome line as my indicator as to whether a person is really logged out.

Currently, an authenticated user, when clicking ``Logout`` in the header, IS logged out and sent to ``user/logout/``
from which there is no escape except to erase the url back to its root (``r'^$'``).

I finally opted for a separate ``logged_out.html`` page which gave me something for my url patterns to target. Here are
the files affected:

**config.urls.py**::

    from django.conf.urls import include, url
    from django.contrib import admin
    from django.views.generic import RedirectView

    urlpatterns = [
        url(r'^$', RedirectView.as_view(pattern_name='dj-auth:login', permanent=False), name='base_url'),
        url(r'^admin/', admin.site.urls),
        url('^activity/', include('activity.urls')),
        url('^user/', include('user.urls', app_name='user', namespace='dj-auth')),
    ]

**user.urls.py**::

    from django.conf.urls import url
    from django.contrib.auth import views as auth_views
    from django.contrib.auth.forms import AuthenticationForm
    from django.views.generic import RedirectView

    urlpatterns = [
        url(r'^k$', RedirectView.as_view(pattern_name='login', permanent=False)),
        url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
        url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logged_out.html'}, name='logout'),
    ]

**user.registration.logged_out.html**::

    {% extends 'user/base_user.html' %}

    {% block title %}Logged Out{% endblock %}

    {% block content %}
        <div class="row">
            <div class="offset-by-four four columns">
                <p><h4 class="center-text u-full-width">You are logged out.</h4></p>
                <form method="get" action="{% url 'base_url' %}">
                    <p>
                        <input class="button-primary u-full-width" value="Login Again" type="submit">
                    </p>
                </form>
            </div>
        </div>

    {% endblock %}

I also did some work on the css getting the Login and Login Again buttons to full width and centering things a little
better.

Requiring Authentiation to Access the Website
---------------------------------------------

Currently, any user who knows the url patterns, or makes a good guess, can get into the website without being
authenticated. For instance, at the login page I can enter ``activity/welcome/`` into the address box and get to the
welcome page without being authenticated. This should be easy to fix since I did it already in ModelExperimentation.

.. csv-table:: **Does submitting a url result in being sent to the Login Page?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, wrap the necessary class views in ``login_required(<view_name>)`` functions in the url patterns
    Yes, but the next=whatever isn't working; implement the changes in *Django Unleashed* Examples 19.47 and 19.48
    Yes, see the affected files below

**user.registration.login.html**::

    ...
    <p class="row">
        {% if next %}
            <input type="hidden" name="next" value="{{ next }}">
        {% endif %}
        <label for="id_username">Username:</label>
        ...

**templates.base.html**::

    ...
    {% if user.is_authenticated %}
        <a class="link" href="{% url 'dj-auth:logout' %}?next={{ request.path }}">Logout</a>
    {% endif %}
    ...

Adding the First Set of Questions
---------------------------------

I will start with the Noah activity since that is the one I have most developed. It currently has a total of five pages,
the first one instructions and the rest are essays. The instruction page is timed. In order to get it to display
properly I will need to:

#. update the information in the page model for the noah pages
#. differentiate between Instruction pages and Essay pages in ``page-display.html``
#. create a Contents(?) model (formerly called Question model) to hold the text of the instructions or questions.

For now I will just keep the listing of the pages and not try to implement keeping track of the user's progress and
displaying the next page accordingly. That means I will have to add a Table of Contents page to the beginning of the
Noah activity and modify ``page-display.html`` accordingly.

Hmm... Thinking about it some I realized that the ``page-display.html`` being fed by the ``PageDisplay`` view isn't
really doing what I wanted. The view sends a set of pages but I really only want one. It seems I may have to figure out
a way either to do away with contents pages, or implement a separate template and view for tables of contents. Activity
types perhaps? Or a 'multi-part' option? I think the latter would be best.

Displaying Activity Overview Page
+++++++++++++++++++++++++++++++++

Narrative: When Jim clicks on "Noah: The REAL Story" he arrives at a page giving him an overview of the entire project
and a list of activities for him to complete. Only the first entry is available the first time he enters the page. As he
completes activities the list of entries indicates his completion with check marks and each new activity opens up in
order.

Refactoring
***********

I noticed that it is simpler to talk about projects and activities rather than activities and pages. I thought of
refactoring the Activity models. But that would be very difficult since I already have an 'activity' app and I don't
want to change it to a 'project' app. I decided to call them 'activities' and 'actions.' I changed the Page model to
the Action model and updated ``activity/views.py``, ``activity/admin.py``, ``activity/urls.py`` and renamed
``page_display.html`` to ``activity_overview.html``. I also changed the ``ActionDisplay`` view into ``ActionOverview``.
Once all this was properly done the website worked as before. Now to get the overview page to display properly.

Basic Overview Page Display
***************************

First I will just implement the looks of the page and get the links to work going to stubs of the action pages. I will
save the actual action pages until later as well as keeping track of which actions have been completed by particular
users.

.. csv-table:: **Does the overview page have an overview optionally at the top of a list of actions?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, modify ``activity_overview.html`` to include it
    No, the ActionOverview view needs to be modified to include the activity in the context
    No, the variable in activity.urls needs to be changed to ``_slug`` along with the ones in the view
    No, getting unexpected 'action_number' keyword argument; create :ref:`new url pattern<overview_url>`
    No, need to fix the link in ``welcome.html`` not to include 'action_number'
    No, activity overview page reached but overview still not visible
    No, in ``ActionOverview`` use :ref:`get()<use_get_not_filter>` instead of filter
    Yes, Now to get the links to work

I will need to work on the css for the overview paragraph later.

Notes:

.. _overview_url:

I had to create a new url pattern when I decided to create an overview page for each activity::

    url(r'^(?P<_slug>[\w\-]+)/$', login_required(ActionOverview.as_view()), name="activity_overview"),

.. _use_get_not_filter:

I was getting the activity to send to ``activity_overview.html`` by using a filter, but filter returns a QuerySet
rather than an object. Change the line in ``ActionOverview`` as follows::

    activity = Activity.objects.get(slug=_slug)

Getting the Links on the Overview Page to Work
++++++++++++++++++++++++++++++++++++++++++++++

This shouldn't be too difficult I don't think. The url pattern already exists but may need to be edited. I'll need a
new view, perhaps 'ActionDisplay.'

.. csv-table:: **Does clicking a link on the overview page get to the proper url 'activity/[slug]/[action number]'?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, edit :ref:`url<action_display_url>`, write the :ref:`ActionDisplay<action_disp_view>`. view, and the stub html
    No, also have to create an actual link in ``activity_overview.html``
    No, got multiple actions; use filter in view: action = Action.objects.filter(slug=_slug).get(number=_action_number)
    No, no slug field in Action; use action = Action.objects.filter(activity=_activity).get(number=_action_number)
    Yes, Next: actually display the actions

.. _action_display_url:

Here is the url for the action_display page::

    url(r'^(?P<_slug>[\w\-]+)/(?P<action_number>[0-9]+)/$',
        login_required(ActivityDisplay.as_view()),
        name="action_display"),


.. _action_disp_view:

The new ActionDisplay view is as follows::

    class ActivityDisplay(View):
        template_name = 'activity/activity_display.html'

        def get(self, request, _slug=None, _action_number=None):
            activity = Activity.objects.get(slug=_slug)
            action = Action.objects.get(number=_action_number)
            return render(request, self.template_name, {'activity':activity, 'action':action})

Implementing the Noah Questions
+++++++++++++++++++++++++++++++

Here is what I had developed earlier for the Noah activity::

    Noah: The Real Story

    Many of you will be familiar with the story of Noah and the Ark in a simplified cartoon or Children’s Bible version,
    but have you read the original?  Now is your chance!  Read Genesis 6:5 - 9:17.  (Click here if you have no idea how
    to find those passages.)  This may take a while, in fact it probably SHOULD take a while so you have time to think
    about what you are reading.  When you are finished come back here and go to the reflection pages by clicking on the
    button below.  (Note: it will be more fun to read the passage before looking at the reflection pages.  You may be
    surprised at the Bible’s version and looking ahead may spoil that.)

        Activity:

        Page One: What did you notice as you were reading the story?  If anything surprised you this would be a good
        place to mention it.

        Page Two: It may have surprised you that this story in the Bible is a bit disjointed.  It jumps from one thing
        to another, gets repetitive, and even contradicts itself, for instance, on the number of each kind of animal
        Noah was to bring on board.  None of this affects the religious value of the story but you may wonder why it is
        that way.  It’s explained in one of the footnotes of the New American Bible translation, but in a way aimed at
        scholars of the Bible.  Read the footnote marked “6:5-8:22" (at the bottom right of page 15 in the editions you
        were given) and try to give a more down-to-earth explanation.  (After all have had a chance to finish, I will
        give my own down-to-earth explanation.)

        Page Three: If we took everything in the Bible literally we would soon be very confused, yet it’s stories still
        have religious value.  You may notice that God does not always seem like Himself in this story: he “regrets”
        things, he sets up something to “remind” Him of his promises.  Why do you think the ancient authors of Scripture
        sometimes spoke in this way?  In other words, what advantage do you see in thinking of God in a very human way?

        Page Four: What lessons might we get from the story of Noah and the Ark?  List as many as you can think of.

From this I see that some items from the introduction need to be on the overview page while others should be on the
first page. The rest of the pages are all "essay" pages.

Here is a revised outline::

    Overview page -- overview and list of five actions

     Action Pages:
        1. Timed instructions to read the page
        2. What they noticed
        3. Interpreting the footnote
        4. Thinking of God in human terms
        5. Lessons from Noah and the Ark

First, after updating the Noah overview, I will work on displaying the timed instructions.

.. csv-table:: **Does clicking the first link on the Noah overview page get to the instructions on reading?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, create a TextField in the action model for the instructions and edit ``activity_display.html`` to show them
    No, change ``{{ activity.text }}`` to ``{{ action.text }}`` in ``action_display.html``. :ref:`see below<name_change_01>`.


.. _name_change_01:

I decided to change the name of ``activity_display.html`` to ``action_display.html`` since that is what it is doing.

Getting the Text on the Action Pages to Format Properly
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

The text on the Action Pages is displaying but it doens't look very good because all the formatting has been removed. I
wonder if there is anything that allows for rich-text format or at least some html formatting commands like <br>. I will
study the Django docs...

I didn't find anything there but *The HTML Pocket Guide* (page 126-128) told me about the <pre> tag and
*The CSS Pocket Guide* (page 158) told me about the white-space property. I will try to use the css approach first.

It worked!  Here is what I used:

In custom.css::

    .formatted {
        white-space: pre-wrap;
    }

In action_display.html::

    <h4 class="formatted">{{ action.text }}</h4>

The page needs to look better. Maybe offset-by-one ten columns at the <h6> size.

Completing the action_display.html Page
---------------------------------------

What this page displays depends on the type of page it is but there are always some navigation buttons visible: 'Next'
and 'Previous.' The 'Previous' button is active on all pages. On the first page it results in going back to the
Welcome page. The 'Next' button is only active if an answer has already been submitted by the current user for this
page. The 'Next' button also submits their current response. Here is a table of page types and objects displayed:

.. csv-table:: **Contents of Various Action Display Pages**
    :header: "Page Type", "Objects Displayed"
    :widths: auto

    Instructions, Formatted Text; Next Button; Previous Button if not first action
    Essay, Formatted Text; TextArea for response; Next Button; Previous Button if not first action
    Multi, Formatted Text; Radio Buttons with possible responses; Next Button; Previous Button if not first action

Implementing the 'Previous' Button
++++++++++++++++++++++++++++++++++

This button appears and is active on all of the pages. Clicking it results in going back to the previous page except on
the first page where it goes back to the Welcome page. Here is the TDD approach:

.. csv-table:: **Does a working 'Previous' button appear on each Action Page?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, add this :ref;`previous button<previous_button> to ``action_display.html`` with ``href="{{ action.previous }}"``
    No, create the ``previous`` function in the Action model
    No, it tried to get to /activity/-slug-/-number-/activity/welcome/; try ``href={% url action.previoue %}``
    No, no reverse; try ``href={{ url action.previouw }}``
    No, syntax error; go back to ``href="{{ action.previous }}`` and use :ref:`this<action_previous>` in the model
    Yes, on to the 'Next' button

.. _action_previous:

Here is a model function to help find the previous page. It wasn't working for a while, would tack the output onto the
current url, but this seems to work::

        def previous(self):
            number = self.number
            slug = self.activity.slug
            if number == 1:
                return '/activity/' + slug + '/'
            else:
                return '/activity/' + slug + '/' + str(number - 1) + '/'

.. _previous_button:

Here is the html for the 'Previous' button::

        <div class="row">
            <a class="button" type="button" href="{{ action.previous }}">Previous</a>
        </div>

Preliminary Implementation of the 'Next' Button
+++++++++++++++++++++++++++++++++++++++++++++++

Full implementation of the 'Next' button will have to wait until I have some means of recording which actions a user
has completed. Here I will just get it displaying and presume they can go to the next page.

.. csv-table:: **Does a working 'Next' button appear on each Action Page?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, add it to ``action_display.html`` and create a model function called next()
    Yes, but instead of going back to the overview page it should go to some sort of congratulation page

.. csv-table:: **Does clicking 'Next' on the last action page for an activity result in a congratulations page?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, it goes to the overview page; create ``congrats.html``, its url, view and edit ``next()`` in the Action model
    Yes, see below: :ref:`congrats.html<congrats>`, :ref:`Congrats view<congrats_view>`, :ref:`next()<new_next>`

.. _congrats:

Here is the inner part of the ``congrats.html`` page::

    {% block content %}

        <div class ="row">
            <h3 class="offset-by-two eight columns">Congratulations, {{ user.first_name }}!</h3>
        </div>
        <div class="row">
            <h4 class = "offset-by-two eight columns">You have completed {{ activity.name }}</h4>
        </div>

    {% endblock %}


.. _congrats_view:

I needed an additional view to render the ``congrats.html`` page::

    class Congrats(View):
        template_name = 'activity/congrats.html'

        def get(self, request, _slug=None):
            _activity = Activity.objects.get(slug=_slug)
            return render(request, self.template_name, {'activity':_activity})


.. _new_next:

And here is the new version of the Action model's `next()` function::

        def next(self):
            number = self.number
            max = len(Action.objects.filter(activity=self.activity))
            slug = self.activity.slug
            if number == max:
                return '/activity/' + slug + '/congrats/'
            else:
                return '/activity/' + slug + '/' + str(number + 1) + '/'

Adding Essay Answers
++++++++++++++++++++

Adding a component for essay questions seems the easiest thing to do first. I will need to:

* display a text box
* display a submit button
* add a view to process the submission of an essay answer
* create the User-Answer model to hold the user's answers

.. csv-table:: **Do essay pages appear with a text box and a submit button?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, add a conditional form to ``action_display.html``
    Yes, get the submit button to do something

.. csv-table:: **Does clicking the 'Submit' button on an Essay page save the essay to the database?**
    :header: "Result", "Action before next test"
    :widths: auto

    No, there is no place to save it; create a UserResponse model
    Yes, but I skipped a lot of mistakes here; see below for the affected files

**The UserResponse Model**::

    class UserResponse(models.Model):
        user = models.ForeignKey(User)
        action = models.ForeignKey(Action, null=True)
        #response = models.ForeignKey(Response)
        essay = models.TextField()

        def __str__(self):
            return self.user.username + "'s response to " + str(self.action)

**The Essay Form in action_display.html**::

    {% if action.type == 'ES' %}
        <div class="row">
            <form class="offset-by-one ten columns" method="post" action="{{ action.get_absolute_url }}submit_essay/">
                <input type="hidden" name="_user" value="{{ user }}">
                <input type="hidden" name="_action" value="{{ action }}">
                <div class="row">
                    <textarea class="u-full-width" name="essay" required autofocus></textarea>
                </div>
                <div class="row">
                    <input class="button-primary offset-by-five two columns u-full-width"
                           type="submit" value="Submit">
                </div>
                {% csrf_token %}
            </form>
        </div>
    {% endif %}

**The SubmitEssay View**::

    class SubmitEssay(View):
        template_name = 'activity/action_display.html'

        def get(self, request):
            return render(request, self.template_name)

        def post(self, request, _slug=None, _action_number=None):
            _activity = Activity.objects.get(slug=_slug)
            _action = Action.objects.filter(activity=_activity).get(number=_action_number)
            new_response = UserResponse(user=request.user,
                                        action=_action,
                                        essay = request.POST['essay'])
            new_response.save()
            return redirect(_action.get_absolute_url())

**The submit_essay URL Pattern**::

    url(r'^(?P<_slug>[\w\-]+)/(?P<_action_number>[0-9]+)/submit_essay/$',
        login_required(SubmitEssay.as_view()),
        name="submit_essay"),

Adding Multiple Choice/True-False Responses
+++++++++++++++++++++++++++++++++++++++++++

This will require another new model to hold the possible responses.



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

.. _moving_to_rectory:

Moving to the Rectory Computer
++++++++++++++++++++++++++++++

I managed to get everything moved over here to my rectory computer, including the data I entered in the database. I
learned that the migration files were not under version control so I had to copy them from my Home computer then did a
``python manage.py migrate`` which worked without difficulty.

Then, using TeamViewer, I got onto my Home computer and created fixtures to serialize the data in the database::

    python manage.py dumpdata activity.Activity > activity.json
    python manage.py dumpdata activity.Page > page.json

According to the Django documentation these were expected in a ``fixtures`` directory under the app where they belonged
(I think) so I created one in the ``activity`` folder, copied the files from my Home computer using TeamViewer (I just
used copy and paste and it worked! New feature in TeamViewer13?), and then copied them to the new ``fixtures``
directory. With all that, loading the data was simple::

    python manage.py loaddata activity.json
    python manage.py loaddata page.json

Random Notes
++++++++++++

.. _table_error:

Apparently one must avoid using double quotes in table entries (at least without escaping them (\"). The first version
of the last line in the :ref:`Welcome Message TDD table<welcome_message_table>` had double quotes around part of it and
generated a warning on ``make html``.
