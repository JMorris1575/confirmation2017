from django.shortcuts import render
from django.views.generic import View
from .models import Activity, Action

# Create your views here.

class WelcomePage(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        activities = Activity.objects.all()
        return render(request, self.template_name, {'activities': activities})

    def post(self, request):
        return render(request, self.template_name)


class ActivityOverview(View):
    template_name = 'activity/activity_overview.html'

    def get(self, request, _slug=None):
        activity = Activity.objects.get(slug=_slug)
        actions = Action.objects.filter(activity__slug=_slug)
        return render(request, self.template_name, {'activity':activity, 'actions':actions})

class ActivityDisplay(View):
    template_name = 'activity/activity_display.html'

    def get(self, request, _slug=None, _action_number=None):
        _activity = Activity.objects.get(slug=_slug)
        action = Action.objects.filter(activity=_activity).get(number=_action_number)
        return render(request, self.template_name, {'activity':_activity, 'action':action})
