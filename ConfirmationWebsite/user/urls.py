from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^k$', RedirectView.as_view(pattern_name='login', permanent=False)),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logged_out.html'}, name='logout'),
]
