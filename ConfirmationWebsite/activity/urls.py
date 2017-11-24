from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .views import(WelcomePage, ActivityOverview, ActivityDisplay, Congrats)

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='welcome_page', permanent=False)),
    url(r'^welcome/$', login_required(WelcomePage.as_view()), name="welcome_page"),
    url(r'^(?P<_slug>[\w\-]+)/$', login_required(ActivityOverview.as_view()), name="activity_overview"),
    url(r'^(?P<_slug>[\w\-]+)/(?P<_action_number>[0-9]+)/$',
        login_required(ActivityDisplay.as_view()),
        name="action_display"),
    url(r'^(?P<_slug>[\w\-]+)/congrats/$', login_required(Congrats.as_view()), name="congrats_page"),
]