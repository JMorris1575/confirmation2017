from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Activity, Action, UserResponse

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
    template_name = 'activity/action_display.html'

    def get(self, request, _slug=None, _action_number=None, _user=None):
        _activity = Activity.objects.get(slug=_slug)
        action = Action.objects.filter(activity=_activity).get(number=_action_number)
        #_essay = UserResponse.objects.filter(user=request.user).get(action=action).essay
        return render(request, self.template_name, {'activity':_activity, 'action':action})

class Congrats(View):
    template_name = 'activity/congrats.html'

    def get(self, request, _slug=None):
        _activity = Activity.objects.get(slug=_slug)
        return render(request, self.template_name, {'activity':_activity})


class SubmitEssay(View):
    template_name = 'activity/action_display.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, _slug=None, _action_number=None):
        _activity = Activity.objects.get(slug=_slug)
        _action = Action.objects.filter(activity=_activity).get(number=_action_number)
        new_response = UserResponse(user=request.user,
                                    action=_action,
                                    essay = request.POST['essay'])
        new_response.save()
        return redirect(_action.next())
