from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/login.html',
         'extra_context': {'form': AuthenticationForm}},
    name='logout'),
]
