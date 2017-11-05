========================================
St. Basil Confirmation Candidate Website
========================================

Starting the Project
====================

This file documents the process used to start the interactive Confirmation page for St. Basil Confirmation Candidates.
It was started on November 4, 2017.

Step One: Creating the Project
------------------------------

I decided to use PyCharm as much as I could and, after creating the project:

`C:\Users\frjam_000\Documents\MyDjangoProjects\StBasilConfirmation`

I went to the help system to learn how to create a virtual environment.

Step Two: Creating a Virtual Environment with PyCharm
-----------------------------------------------------

I wanted to create a new virtual environment called `conf` for Python 3.6. In the Settings dialog box I clicked on the
projects name and then on Interpreter. I had to click the gear icon at the upper right and selected Create VirtualEnv.
I learned I had to put `Envs` into the pathname myself or the new environment would be created in the `frjam_000`
directory. (I had to delete the `conf` environment I created there.) I selected Python 3.6 as the Base interpreter and
clicked OK.

That seemed to do it, and the terminal was already in the virtual environment.

I just checked, and `workon conf` in a command window activates the virtual environment too.

Step Three: Installing and Using Sphinx
---------------------------------------

I wanted to be able to start writing these documents so my first pip install was:

`pip install sphinx`

This installed Sphinx 1.6.5.

To get the project directory structure I like I had to use PyCharm to create a `docs` directory in the
`StBasilConfirmation` directory and, in the teminal type:

`cd docs`
`sphinx-quickstart`

I used all the defaults and called the project: **St. Basil Confirmation Candidate Website** with the author:
**Fr. Jim Morris**.

I added `startup.rst` to the contents in the index.rst file and now I will try using the `make html` command from the
PyCharm terminal...

It worked perfectly! I will probably want to make some changes in `conf.py` eventually but, for now, what I have will
serve the purpose.

Step Four: Initiating Version Control
-------------------------------------

I clicked `VCS -> Initiate Version Control` (or whatever it said -- it disappeared from the menu after I clicked it)
and selected Git as my version control system. All the untracked files lit up in red.

I created a `.gitignore` file in the `StBasilConfirmation` directory and populated it with the following::

    docs/_build/html/_sources/
    docs/_build/html/_static/
    .idea/

Then I did the first commit.

It's getting close to time for Confessions so I will save the rest of the startup process for later.

Step Five: Installing Django
----------------------------

Django is easy to install. In PyCharm's Terminal I first verified it was in the `conf` virtual environment then typed:

`pip install django`

It seemed to take a while but it installed Django 1.11.7 without problems.

Step Six: Creating the Django Project
-------------------------------------

In the PyCharm terminal I typed:

`django-admin startproject StBasilConfirmation`

which it did so quickly I wondered if it had done it correctly, especially since nothing showed up in the Project window
until I clicked on it.

I then realized it may be confusing to have the Django project name the same as the PyCharm project name and decided to
erase the Django project by deleting the `StBasilConfirmation` folder created by `startproject`. I repeated the process
with:

`django-admin startproject ConfirmationWebsite`

and then set about making the necessary changes and additions.

Changing the Name of the Configuration Folder
+++++++++++++++++++++++++++++++++++++++++++++

Using PyCharm's Refactor to change the inner `ConfirmationWebsite` folder to `config` found all the necessary changes
in the other files and was very easy to perform. (Well, almost. I added the previous sentence before clicking "Do
Refactor" and it complained that the code had changed and that I had to search over again.)

Installing psycopg2
+++++++++++++++++++

I tried simply doing:

`pip install psycopg2-2.7.3-cp36-cp36m-win_amd64.whl`

in PyCharm's terminal while in the project directory `C:\Users\frjam_000\Documents\MyDjangoProjects\StBasilConfirmation`
but it could not find the file

`pip install c:/psycopg2-2.7.3-cp36-cp36m-win_amd64.whl`

worked right away.

Changing to PostgreSQL
++++++++++++++++++++++

Preparing the Local Database
****************************

In pgAdmin III I double-clicked `PostgreSQL 9.5 (localhost:5432)` and entered my password (dylan selfie), right-clicked
on `Databases` and selected `New Database...`. I called it `confdatabase`, named Jim as the owner, and added the
comment: `Created on the rectory computer for the St. Basil Confirmation Website.`

Database Changes in Settings.py
*******************************

This is going to involve adding the `secrets.json` file and dividing the `settings.py` file into three files in a new
`settings` module. I will include the database changes when I do all of that.

