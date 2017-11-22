from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .views import(WelcomePage, PageDisplay)

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='welcome_page', permanent=False)),
    url(r'^welcome/$', login_required(WelcomePage.as_view()), name="welcome_page"),
    url(r'^(?P<slug>[\w\-]+)/(?P<page_number>[0-9]+)/$', login_required(PageDisplay.as_view()), name="page_display"),
]