from django.conf.urls import url
from .views import(WelcomePage, )

urlpatterns = [
    url(r'^welcome/$', WelcomePage.as_view(), name="welcome_page")
]