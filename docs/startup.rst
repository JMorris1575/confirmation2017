Starting the Confirmation Project
=================================

This file documents the process used to start the interactive Confirmation page for St. Basil Confirmation Candidates.
It was started on November 4, 2017.

Step One: Creating the Project
------------------------------

I decided to use PyCharm as much as I could and, after creating the project:

``C:\Users\frjam_000\Documents\MyDjangoProjects\StBasilConfirmation``

I went to the help system to learn how to create a virtual environment.

Step Two: Creating a Virtual Environment with PyCharm
-----------------------------------------------------

I wanted to create a new virtual environment called ``conf`` for Python 3.6. In the Settings dialog box I clicked on the
projects name and then on Interpreter. I had to click the gear icon at the upper right and selected Create VirtualEnv.
I learned I had to put ``Envs`` into the pathname myself or the new environment would be created in the ``frjam_000``
directory. (I had to delete the ``conf`` environment I created there.) I selected Python 3.6 as the Base interpreter and
clicked OK.

That seemed to do it, and the terminal was already in the virtual environment.

I just checked, and ``workon conf`` in a command window activates the virtual environment too.

Step Three: Installing and Using Sphinx
---------------------------------------

I wanted to be able to start writing these documents so my first pip install was:

``pip install sphinx``

This installed Sphinx 1.6.5.

To get the project directory structure I like I had to use PyCharm to create a ``docs`` directory in the
``StBasilConfirmation`` directory and, in the teminal type:

``cd docs``
``sphinx-quickstart``

I used all the defaults and called the project: **St. Basil Confirmation Candidate Website** with the author:
**Fr. Jim Morris**.

I added ``startup.rst`` to the contents in the index.rst file and now I will try using the ``make html`` command from the
PyCharm terminal...

It worked perfectly! I will probably want to make some changes in ``conf.py`` eventually but, for now, what I have will
serve the purpose.

Step Four: Initiating Version Control
-------------------------------------

I clicked ``VCS -> Initiate Version Control`` (or whatever it said -- it disappeared from the menu after I clicked it)
and selected Git as my version control system. All the untracked files lit up in red.

I created a ``.gitignore`` file in the ``StBasilConfirmation`` directory and populated it with the following::

    docs/_build/html/_sources/
    docs/_build/html/_static/
    .idea/

Then I did the first commit.

It's getting close to time for Confessions so I will save the rest of the startup process for later.

Step Five: Installing Django
----------------------------

Django is easy to install. In PyCharm's Terminal I first verified it was in the ``conf`` virtual environment then typed:

``pip install django``

It seemed to take a while but it installed Django 1.11.7 without problems.

Step Six: Creating the Django Project
-------------------------------------

In the PyCharm terminal I typed:

``django-admin startproject StBasilConfirmation``

which it did so quickly I wondered if it had done it correctly, especially since nothing showed up in the Project window
until I clicked on it.

I then realized it may be confusing to have the Django project name the same as the PyCharm project name and decided to
erase the Django project by deleting the ``StBasilConfirmation`` folder created by ``startproject``. I repeated the process
with:

``django-admin startproject ConfirmationWebsite``

and then set about making the necessary changes and additions.

Changing the Name of the Configuration Folder
+++++++++++++++++++++++++++++++++++++++++++++

Using PyCharm's Refactor to change the inner ``ConfirmationWebsite`` folder to ``config`` found all the necessary changes
in the other files and was very easy to perform. (Well, almost. I added the previous sentence before clicking "Do
Refactor" and it complained that the code had changed and that I had to search over again.)

Installing psycopg2
+++++++++++++++++++

I tried simply doing:

``pip install psycopg2-2.7.3-cp36-cp36m-win_amd64.whl``

in PyCharm's terminal while in the project directory ``C:\Users\frjam_000\Documents\MyDjangoProjects\StBasilConfirmation``
but it could not find the file

``pip install c:/psycopg2-2.7.3-cp36-cp36m-win_amd64.whl``

worked right away.

Changing to PostgreSQL
++++++++++++++++++++++

Preparing the Local Database
****************************

In pgAdmin III I double-clicked ``PostgreSQL 9.5 (localhost:5432)`` and entered my password (dylan selfie), right-clicked
on ``Databases`` and selected ``New Database...``. I called it ``confdatabase``, named Jim as the owner, and added the
comment: ``Created on the rectory computer for the St. Basil Confirmation Website.``

Database Changes in Settings.py
*******************************

This is going to involve adding the ``secrets.json`` file and dividing the ``settings.py`` file into three files in a new
``settings`` module. I will include the database changes when I do all of that.

Step Seven: Restructuring the Django Settings
---------------------------------------------

As before, I want to move the ``settings.py`` file into a separate ``settings`` folder with an ``__init__.py`` file to
make it a package or module, I don't remember which, and create seperate settings files for development and production.
While I'm at it I might as well create the ``conf-secrets.json`` file to protect the secrets, rather than having them
displayed on GitHub. Alas, now that I mention that I realize I have already published the current ``settings.py`` file
on GidHub, along with the ``SECRET_KEY``. I will have to change that after I create ``conf-secrets.json``. I think
there was a method listed in `Django Unleashed`.

Creating the settings Module
++++++++++++++++++++++++++++

I added a new directory called ``settings`` to the ``config`` directory and added an ``__init__.py`` file containing::

    """
    Uncomment the appropriate line according to which machine is being used.
    On the development machine, use dev.py, on the production machine, use prod.py
    """

    from .dev import *

    # from .prod import *

This was copied from ``c17Development`` but with the instructional comment edited.

base.py
+++++++

I copied the ``settings.py`` file created by Django 1.11 and copied it to ``base.py``. Then I went through and changed
it to the following::

    """
    Django settings for ConfirmationWebsite project.

    Generated by 'django-admin startproject' using Django 1.11.7.

    For more information on this file, see
    https://docs.djangoproject.com/en/1.11/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/1.11/ref/settings/
    """

    import os

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Added as per instructions in Two Scoops of Django chapter 5

    import json

    from django.core.exceptions import ImproperlyConfigured
    from django.core.urlresolvers import reverse_lazy

    # JSON-based secrets module
    with open(os.path.join(BASE_DIR, 'config/settings/conf-secrets.json')) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        """Get the secret variable or return explicit excepton."""
        try:
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {0} variable in the secret file".format(setting)
            raise ImproperlyConfigured(error_msg)


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = get_secret("SECRET_KEY") # 'v5mzgm)jfqcp2^=mrh2cl+q!7i^1wj$5&egyw02=n_wb)b3_zu'

    ALLOWED_HOSTS = []


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'config.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'config.wsgi.application'


    # Password validation
    # https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/1.11/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'America/Detroit'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

dev.py
++++++

I copied ``dev.py`` from Christmas2017 and edited it to what follows::

    from .base import *

    import os

    # SECURITY WARNING: don't run with debug turnd on in production!
    DEBUG = True

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': get_secret('DATABASE_NAME'),
            'USER': get_secret('DATABASE_USER'),
            'PASSWORD': get_secret('DATABASE_PASSWORD'),
            'HOST': get_secret('DATABASE_HOST'),
            'PORT': get_secret('DATABASE_PORT')
        }
    }

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.11/howto/static-files/

    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', 'site'), )

prod.py
+++++++

Similarly, I copied ``prod.py`` from Christmas2017 and edited it as follows. Note that I commented some lines out until
I know what they should contain::

    from .base import *

    import os

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': get_secret('PROD_DATABASE_NAME'),
            'USER': get_secret('PROD_DATABASE_USER'),
            'PASSWORD': get_secret('PROD_DATABASE_PASSWORD'),
            'HOST': get_secret('PROD_DATABASE_HOST'),
            'PORT': get_secret('PROD_DATABASE_PORT')
        }
    }

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.11/howto/static-files/

    # STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'c17_static/')
    # STATIC_URL = 'http://christmas.jmorris.webfactional.com/static/'
    STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'static', 'site',), )

    # ALLOWED_HOSTS.append('christmas.jmorris.webfactional.com')

    ADMINS = (
        ('Jim', 'jmorris@ecybermind.net'), ('Jim', 'frjamesmorris@gmail.com')
    )


    EMAIL_HOST = get_secret('EMAIL_HOST')
    EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = get_secret('DEFAULT_FROM_EMAIL')
    SERVER_EMAIL = get_secret('SERVER_EMAIL')

conf-secrets.json
+++++++++++++++++

Finally, I copied ``secrets.json`` from Christmas2017 into ``conf-secrets.json`` and edited it for the Confirmation
Website. I will not copy it here.

To update the ``SECRET_KEY`` I used the second technique given on page 736 of `Django Unleashed`. In PyCharm's Terminal
I got into the Django shell ``python manage.py shell`` then typed::

    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    get_random_string(50, chars)

and it obediently printed out a new ``SECRET_KEY`` which I copied into ``conf-secrets.json``.

Testing the Website
+++++++++++++++++++

I typed ``python manage.py runserver`` in PyCharm's Terminal and, upon visiting ``localhost:8000`` I got the "It
worked! message. Yay!

Now I will delete the original ``settings.py`` file and do a commit.
