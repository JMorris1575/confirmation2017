Planning the Confirmation Website
=================================

This document details the plans for the Confirmation Website for St. Basil Catholic Church, 2017. It will help design
the database structures and plan the whole Django program.

Narrative Walkthroughs
----------------------

Initial Walkthrough from WordPerfect
++++++++++++++++++++++++++++++++++++

Jim the Confirmation Candidate enters the St. Basil Confirmation website by clicking a link on the parish’s own website.
(Determine where.) Upon arriving at the site he is asked to login with the username and password provided to him by the
church.

Once he logs in he is welcomed to a page that shows the currently existing projects with checkmarks indicating his
progress through them. When he clicks on the “Continue” button he comes to the page of his next uncompleted step. He can
page backward through completed steps and perhaps edit his written out answers, but he cannot go ahead to pages he has
not finished until he has completed the ones leading up to it. He finished the last project and is now ready to start
“The Real Story of Noah.”  He clicks the “Continue” button.

[Alternative: Once he logs in he is welcomed to a page that shows the currently existing projects with checkmarks next
to ones he has finished and percentage of completion otherwise. He can select any project by clicking on its name.  He
clicks on the “The Real Story of Noah” which he is just beginning.]

Jim arrives at a page explaining what he must do, read the story of Noah in the Bible and, when he is finished, he
clicks on the “Next” button.

Jim arrives at a page asking him a question or requests his point of view or otherwise asks him to write something.
Sometimes questions may be multiple choice or even True or False. He responds and clicks on the “Submit” button.

He is brought to the next page which may or may not give him feedback on the previous question and presents a new
question or activity. Jim... [This is where the WordPerfect file ends.]

Miguel
++++++

Miguel, a St. Basil Confirmation candidate, decides to visit the parish's Confirmation candidate website. Upon entering
the site he sees a red banner heading with "St. Basil Confirmation Candidate Website" at the top with a Holy Spirit
image to the left. Below that is a form asking for his username and password. He enters these as they were given to him
in an e-mail, or possibly even via regular mail. When he clicks the Submit button he enters the site proper.

The first page he sees lists a set of activities he can accomplish. Since this is his first time at the site, they all
indicate that he is 0% finished with that activity.

He decides to select the activity labelled "Noah: The REAL Story" and enters the opening page of that activity. This
first page simply tells him to read a passage from the bible (there is a link on the page pointing to an explanation of
how to find passages in the bible). It instructs him to click on the "Finished Reading" button only after he has
completed reading the passage. Behind the scenes the computer has stored the date and time he first entered the page and
will record the date and time he clicks the "Finished Reading" button. This can be used to help ensure the candidates
really read the passage.

Miguel leaves the page and goes to his bible to read the passage. Afterwards he returns to the website and enters the
"Noah: The REAL Story" activity again. It opens to the first page, the one with the "Finished Reading" button, which he
now clicks.

The next page asks him to read and simplify one of the footnotes in his bible. It has a box with the instructions and
a text entry box for him to enter his answer. When he clicks "Submit" his response is stored (though he can edit it
later) and he proceeds to the third page.

This one is simpler. It asks him a multiple choice question and allows him to select one of the answers. He is tired,
however, and he still has other homework to do, so he leaves the site for another day.

Mary
++++

Mary, also a St. Basil Confirmation Candidate, has visited the website several times. When she logs in to the site she
sees the page with all the activities she has worked on with 100% next to the ones she has completed and some other
number indicating how much she has completed next to any she has started. She clicks on one that says 60% and goes
immediately to page four out of five. She has completed the other three.

But Mary isn't happy with her answer to the previous page's question so she clicks the "Previous" button at the bottom
left and goes to the preceding question. There she can edit her answer since it was an open-ended "what are your
thoughts" kind of question. Multiple choice questions cannot be changed because the correct answers are given jsut after
the candidates have submitted their response.

When she has edited her response she clicks the "Next" button to go back to page four and answers that question, a True
False type.

Fr. Jim
+++++++

As one of the administrators of the site, Fr. Jim has more choices than the candidates do. He can send out e-mails (to
which the other adults involved may also have access for safe environment purposes). Fr. Jim, and at least some of the
others also has access to a summary page of all the candidates activities. He can also comment on candidate responses
and perhaps send individual e-mails to that candidate when he has made a comment on his or her responses.

Thoughts After the Walkthroughs
-------------------------------

The main page seems simple enough to implement. A table should be able to hold the names of the activities and the
percent completed.

Each page will have the same header and footer which can be implemented as it has in my Christmas websites.

The challenge will be in the different kinds of activity pages. Somehow, each activity needs to know what kind of page
to display and have the right kind of content available for that kind of page. There should be a timing option so that
the time it takes the candidates to respond can be tracked and used if desired. Also, the aftermath of clicking the
"Submit" button may differ from page to page, or at least from one type of page to another. Pages requesting text
input should allow administrator comments, which closes that page for editing. Multiple Choice pages may optionally
give the correct answer once the candidates have submitted their response. All these differences will have to be
programmed in to the models somehow.

I think I have enough of an idea now to think about the database models I need to design. It will probably be much like
what I have already designed for the Christmas 2017 website.

Model Design
------------

Initial Thoughts
++++++++++++++++

I will need a User model which, in addition to the user name, e-mail and password will have to keep some information
on what the candidate has accomplished so far, where they stand in the various categories and perhaps even their
responses to each question. On second thought, much of that information can be kept in other models: who made a response
in a Response model, the time of entering and leaving timed pages for instance, but some things may still need to be
kept in a supplement to Django's ``auth.user`` model.

There will need to be a model for the different types of pages: the instruction page, the text input page, the multiple
choice page. Some of these will have to have the ability to store usage dates and times corresponding to each user.

Data Listing
++++++++++++

A quick glance of Chapter 30 of *Django Unleashed* suggested, at least to me, that it might be helpful to simply list
the data that needs to be recorded without much concern as to models at the beginning. Here is an attempt to do that::

    What Needs to be Remembered

    The activities
    The pages for each activity
    The type of page: instructions, open answer, multiple choice/true-false, timed
    Suggested answers for multiple choice questions
    User history: pages completed, date-time of entry and leaving pages marked
    User Responses

Models to Test
++++++++++++++

I have just completed my Model Experimentation project that it may be able to be used to test the models I develop here.
Here are my initial model ideas::

    * Augment the User model to keep track of the last page completed in each activity the number of pages completed
    * Create an Activity model with the name of that activity
    * Create a Page model connected to an Activity and an indicator as to the type of page
    * Create a Question model with the text of the question and the page on which it appears
    * Create a Response model with the question to which it belongs, a possible response, and whether this response
    is correct
    true/false questions
    * Create an Essay model pointing to the question to which it belongs and a space for the answers and the user who
    answers this way
    * Create a User_Answers model with activity, page, their response to that page and whether their answer was correct
    * Allow for an anonymous User for essay questions or comments that should remain anonymous

So, here goes:

.. csv-table:: **Activity Model**
    :header: "Field Name", "Type", "Parameters", "Notes"
    :widths: auto

    number, IntegerField, primary_key=True, so that activities can be re-ordered
    name, CharField, max_characters=30, the name to be displayed in the list and headings

|

.. csv-table:: **Page Model**
    :header: "Field Name", "Type", "Parameters", "Notes"
    :widths: auto

    activity, "ForeignKey", 'Activity', the activity to which this page belongs
    type, CharField, , the type of page: INSTRUCTIONS; MULTICHOICE; ESSAY; ANONYMOUS
    timed, Boolean, , True if this page is to be timed; False otherwise

|

.. csv-table:: **Question Model**
    :header: "Field Name", "Type", "Parameters", "Notes"
    :widths: auto

    page, ForeignKey, 'Page', the page on which this question appears
    text. CharField, max_length=400, the text of the question

|

.. csv-table:: **Response Model**
    :header: "Field Name", "Type", "Parameters", "Notes"
    :widths: auto

    question, ForeignKey, 'Question', the question to which this is a possible response
    text, CharField, max_length=100, the text of the possible response
    correct, Boolean, , True if this is the correct response; False otherwise

|

.. csv-table:: **Essay Model**
    :header: "Field Name", "Type", "Parameters", "Notes"
    :widths: auto

    question, ForeignKey, 'Question', the question to which this response belongs
    user, ForeignKey, 'User', the user responding (could be anonymous)
    text, TextField, , the response

|

.. csv-table:: **User-Answer Model**
    :header: "Field Name", "Type", "Parameters", "Notes"
    :widths: auto

    user, ForeignKey, 'User', the user making this response
    question, ForeignKey, 'Question', the question to which this response belongs
    response, ForeignKey, 'Response', the response they chose to questions on MULTICHOICE pages
    essay, ForeignKey, 'Essay', the text they wrote to questions on ESSAY pages
    time, DateTimeField?, , the time it took them to complete a TIMED page

|

.. csv-table:: **User_Profile Model**
    :header: "Field Name", "Type", "Parameters", "Notes"
    :widths: auto

    total_pages, IntegerField, , total number of pages completed
    last_page, ForeignKey, 'Page', last page completed

|

What I Learned from the Models Above
++++++++++++++++++++++++++++++++++++

**Activity Model**: I may have to develop some means of breaking larger activities into sub-activities but I will definitely
have to figure out how to make some choices unavailable if the candidate has not completed its prerequisites -- so that,
for instance, Abraham Episode 3 cannot be done before Episodes 1 or 2.  That presumes, however, that the unavailable
ones will be listed together with the available ones. That is not necessarily the case. I could put the different
episodes into a page sequence and ensure, somehow, that the pages have to be completed in order.

**Activity Model**: I need to add a slug field to the Activity Model so that it can be used to identify the different
activities in the url. It should be based on the name of the activity and added/computed when the activity is created.





URLs
----

Here is my first attempt to plan the URL scheme of the website:

.. csv-table:: **URL Patterns - First Attempt**
   :header: "URL", "Page(s) Addressed", "Notes"
   :widths: auto

    /, login.html, Entering the site brings them to the login page
    /login, login.html, This is the URL to which / redirects
    /main, activities.html, The page with the list of activities
    /<activity-slug>/create, activity_create.html, page where administrators can create new activities
    /<activity-slug>/<n>, <page-type>.html, <page-type> selected by activity and page number <n>
    /<activity-slug/<n>/create, <create-page-type>.html, pages for administrators to create new pages




