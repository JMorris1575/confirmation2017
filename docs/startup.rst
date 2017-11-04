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