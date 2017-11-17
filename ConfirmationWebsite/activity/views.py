from django.shortcuts import render
from django.views.generic import View
from .models import Activity, Page

# Create your views here.

class WelcomePage(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        activities = Activity.objects.all()
        return render(request, self.template_name, {'activities': activities})

    def post(self, request):
        return render(request, self.template_name)


class PageDisplay(View):
    template_name = 'activity/page_display.html'

    def get(self, request, slug=None, page_number=None):
        pages = Page.objects.filter(activity__slug=slug)
        return render(request, self.template_name, {'pages':pages})