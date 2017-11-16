from django.shortcuts import render
from django.views.generic import View
from .models import Activity

# Create your views here.

class WelcomePage(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        activities = Activity.objects.all()
        return render(request, self.template_name, {'activities': activities})

    def post(self, request):
        return render(request, self.template_name)