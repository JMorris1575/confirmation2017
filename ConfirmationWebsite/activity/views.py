from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class WelcomePage(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)